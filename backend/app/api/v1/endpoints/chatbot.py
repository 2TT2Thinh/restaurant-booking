# app/api/v1/endpoints/chatbot.py
"""
Chatbot endpoint.

State management: STATELESS on server. The client sends the full
conversation history with every request. This avoids server-side
session storage and scales horizontally without sticky sessions.

Client flow:
  1. User types message
  2. Client appends { role: "user", content: "..." } to local history
  3. Client POST /chat with full history
  4. Server returns { reply, booking_intent }
  5. Client appends { role: "assistant", content: reply } to local history
  6. If booking_intent is set, client shows "Book this?" confirmation button
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from app.api import deps
from app.core.config import settings
from app.models.user import User
from app.services.chatbot_service import process_chat_message

router = APIRouter()


class ChatMessage(BaseModel):
    role:    str            # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(
        ...,
        min_length=1,
        max_length=20,      # prevent token abuse — max 20 turns per request
        description="Full conversation history including the new user message"
    )


class BookingIntent(BaseModel):
    """Populated when Claude has identified a specific slot to book."""
    restaurant_id: Optional[int]  = None
    booking_date:  Optional[str]  = None   # YYYY-MM-DD
    booking_time:  Optional[str]  = None   # HH:MM
    guests:        Optional[int]  = None


class ChatResponse(BaseModel):
    reply:          str
    booking_intent: Optional[BookingIntent] = None


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession    = Depends(deps.get_db),
    current_user: User  = Depends(deps.get_current_user),
):
    """
    Send a message to the booking assistant.
    Returns a natural language reply and optionally a booking_intent
    that the frontend can use to pre-fill the booking form.
    """
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chatbot service is not configured",
        )

    # Convert to dict format expected by Claude API
    messages_dict = [
        {"role": m.role, "content": m.content}
        for m in request.messages
    ]

    result = await process_chat_message(
        messages=messages_dict,
        db=db,
        user_id=current_user.id,
        api_key=settings.ANTHROPIC_API_KEY,
    )

    intent_data = result.get("booking_intent")
    booking_intent = BookingIntent(**intent_data) if intent_data else None

    return ChatResponse(
        reply=result["reply"],
        booking_intent=booking_intent,
    )