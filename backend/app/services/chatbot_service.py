# app/services/chatbot_service.py
"""
Booking assistant chatbot powered by Claude API.

Architecture:
  - Claude acts as the reasoning/NLP layer
  - Your existing services (recommendation, smart_booking) are the tools
  - Tool results are real DB data — Claude only formats the response
  - Conversation history is maintained by the client (stateless server)

Tool definitions exposed to Claude:
  1. search_restaurants    — filter by cuisine, name
  2. check_slot            — occupancy for a specific slot
  3. suggest_time_slots    — alternatives for a busy slot
  4. get_recommendations   — personalized restaurant ranking

The client sends: { messages: [...], user_context: { user_id, today } }
The server returns: { reply: str, suggestions: [...], booking_intent: {...} | null }
"""
import json
from datetime import date, time, datetime
from typing import Any, Optional

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_restaurant import get_all_restaurants
from app.services.recommendation_service import get_recommendations
from app.services.smart_booking_service import (
    analyze_slot,
    suggest_time_slots,
    suggest_dates,
)

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL   = "claude-sonnet-4-20250514"

# ── Tool definitions (sent to Claude API) ────────────────────────────────────

TOOLS = [
    {
        "name": "search_restaurants",
        "description": (
            "Search for restaurants by name or cuisine type. "
            "Use this when the user mentions a specific cuisine or restaurant name."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "search": {
                    "type": "string",
                    "description": "Restaurant name or cuisine keyword (e.g. 'Việt Nam', 'Nhật', 'pizza')"
                },
                "limit": {"type": "integer", "default": 5}
            },
            "required": []
        }
    },
    {
        "name": "get_recommendations",
        "description": (
            "Get personalized restaurant recommendations for the current user. "
            "Use this when the user asks for suggestions without specifying a restaurant."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "for_date": {
                    "type": "string",
                    "description": "ISO date string YYYY-MM-DD. Defaults to today."
                },
                "limit": {"type": "integer", "default": 5}
            },
            "required": []
        }
    },
    {
        "name": "check_slot_availability",
        "description": (
            "Check how busy a specific restaurant is at a given date and time. "
            "Returns occupancy rate, available seats, and whether it's peak hour."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "integer"},
                "booking_date":  {"type": "string", "description": "YYYY-MM-DD"},
                "booking_time":  {"type": "string", "description": "HH:MM"},
                "guests":        {"type": "integer", "default": 2}
            },
            "required": ["restaurant_id", "booking_date", "booking_time"]
        }
    },
    {
        "name": "suggest_alternative_times",
        "description": (
            "When a time slot is too busy, find less crowded alternatives "
            "on the same day within ±3 hours."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "integer"},
                "booking_date":  {"type": "string", "description": "YYYY-MM-DD"},
                "booking_time":  {"type": "string", "description": "HH:MM"},
                "guests":        {"type": "integer", "default": 2}
            },
            "required": ["restaurant_id", "booking_date", "booking_time"]
        }
    },
]

SYSTEM_PROMPT = """Bạn là trợ lý đặt bàn nhà hàng thông minh. Nhiệm vụ của bạn:
1. Hiểu yêu cầu của người dùng (nhà hàng, ngày, giờ, số người)
2. Dùng các công cụ (tools) để tìm nhà hàng và kiểm tra chỗ trống
3. Trả lời ngắn gọn, thân thiện bằng tiếng Việt
4. Luôn đề xuất các lựa chọn cụ thể với thông tin đầy đủ
5. Nếu khung giờ đông, chủ động gợi ý khung giờ ít đông hơn

Khi trả lời, format như sau:
- Dùng emoji để dễ đọc (🍜 🕐 👥 ✅ ⚠️)
- Liệt kê options rõ ràng nếu có nhiều lựa chọn
- Kết thúc bằng câu hỏi xác nhận hoặc hỏi thêm thông tin nếu cần

Ngày hôm nay: {today}"""


# ── Tool executor ─────────────────────────────────────────────────────────────

async def _execute_tool(
    tool_name: str,
    tool_input: dict,
    db: AsyncSession,
    user_id: int,
) -> Any:
    """Routes tool calls from Claude to actual service functions."""

    if tool_name == "search_restaurants":
        items, total = await get_all_restaurants(
            db,
            search=tool_input.get("search"),
            limit=tool_input.get("limit", 5),
        )
        return [
            {
                "id":           r.id,
                "name":         r.name,
                "cuisine_type": r.cuisine_type,
                "address":      r.address,
                "max_capacity": r.max_capacity,
                "opening_time": str(r.opening_time) if r.opening_time else None,
                "closing_time": str(r.closing_time) if r.closing_time else None,
            }
            for r in items
        ]

    if tool_name == "get_recommendations":
        for_date_str = tool_input.get("for_date")
        for_date = date.fromisoformat(for_date_str) if for_date_str else date.today()
        results = await get_recommendations(
            db, user_id=user_id, limit=tool_input.get("limit", 5), for_date=for_date
        )
        return [
            {
                "id":            r["restaurant"].id,
                "name":          r["restaurant"].name,
                "cuisine_type":  r["restaurant"].cuisine_type,
                "address":       r["restaurant"].address,
                "score":         r["score"],
                "reason":        r["reason"],
                "available_seats": r["available_seats"],
            }
            for r in results
        ]

    if tool_name == "check_slot_availability":
        analysis = await analyze_slot(
            db,
            restaurant_id=tool_input["restaurant_id"],
            booking_date=date.fromisoformat(tool_input["booking_date"]),
            booking_time=time.fromisoformat(tool_input["booking_time"]),
            guests=tool_input.get("guests", 2),
        )
        return {
            "available":      analysis.available,
            "booked_guests":  analysis.booked_guests,
            "max_capacity":   analysis.max_capacity,
            "occupancy_rate": analysis.occupancy_rate,
            "is_peak":        analysis.is_peak,
            "label":          analysis.label,
        }

    if tool_name == "suggest_alternative_times":
        slots = await suggest_time_slots(
            db,
            restaurant_id=tool_input["restaurant_id"],
            booking_date=date.fromisoformat(tool_input["booking_date"]),
            preferred_time=time.fromisoformat(tool_input["booking_time"]),
            guests=tool_input.get("guests", 2),
        )
        return [
            {
                "time":          str(s.booking_time)[:5],
                "available":     s.available,
                "occupancy_rate": s.occupancy_rate,
                "label":         s.label,
            }
            for s in slots
        ]

    return {"error": f"Unknown tool: {tool_name}"}


# ── Main chat function ────────────────────────────────────────────────────────

async def process_chat_message(
    messages: list[dict],        # full conversation history from client
    db: AsyncSession,
    user_id: int,
    api_key: str,                # Anthropic API key from settings
) -> dict:
    """
    Sends conversation to Claude with tools defined.
    Handles tool calls in an agentic loop (max 5 iterations).
    Returns { reply: str, booking_intent: dict | None }
    """
    today = date.today().isoformat()
    system = SYSTEM_PROMPT.format(today=today)

    working_messages = list(messages)
    booking_intent   = None

    async with httpx.AsyncClient(timeout=30.0) as client:
        for iteration in range(5):  # max tool-call iterations
            response = await client.post(
                CLAUDE_API_URL,
                headers={
                    "x-api-key":         api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type":      "application/json",
                },
                json={
                    "model":      CLAUDE_MODEL,
                    "max_tokens": 1024,
                    "system":     system,
                    "tools":      TOOLS,
                    "messages":   working_messages,
                },
            )
            response.raise_for_status()
            data = response.json()

            stop_reason = data.get("stop_reason")
            content     = data.get("content", [])

            # ── If Claude wants to use a tool ────────────────────────────────
            if stop_reason == "tool_use":
                # Add Claude's response (with tool_use blocks) to history
                working_messages.append({"role": "assistant", "content": content})

                # Execute all tool calls and collect results
                tool_results = []
                for block in content:
                    if block.get("type") != "tool_use":
                        continue

                    tool_result = await _execute_tool(
                        tool_name=block["name"],
                        tool_input=block["input"],
                        db=db,
                        user_id=user_id,
                    )

                    # Extract booking intent if Claude checked a specific slot
                    if block["name"] == "check_slot_availability":
                        booking_intent = {
                            **block["input"],
                            "availability": tool_result,
                        }

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": block["id"],
                        "content":     json.dumps(tool_result, ensure_ascii=False, default=str),
                    })

                # Feed tool results back to Claude
                working_messages.append({"role": "user", "content": tool_results})
                continue  # next iteration — Claude will now form a response

            # ── Claude gave a final text response ────────────────────────────
            if stop_reason == "end_turn":
                reply_text = " ".join(
                    block.get("text", "")
                    for block in content
                    if block.get("type") == "text"
                ).strip()

                return {
                    "reply":          reply_text,
                    "booking_intent": booking_intent,
                }

    return {
        "reply":          "Xin lỗi, tôi không thể xử lý yêu cầu lúc này. Vui lòng thử lại.",
        "booking_intent": None,
    }