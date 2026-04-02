# app/services/chatbot_service.py
import asyncio
import logging
from functools import partial
from datetime import date, datetime
from typing import Optional

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.services.recommendation_service import get_recommendations

# Setup logging
logger = logging.getLogger(__name__)

# Config from settings (TASK 4)
INTERNAL_BASE = settings.INTERNAL_BASE_URL.rstrip("/")
OLLAMA_URL    = f"{settings.OLLAMA_HOST}/api/generate"
OLLAMA_MODEL  = settings.OLLAMA_MODEL_NAME

# HTTP Client pool
_http_client: Optional[httpx.AsyncClient] = None
_sync_client: Optional[httpx.Client] = None

async def get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(10.0, read=30.0),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
    return _http_client

def get_sync_client() -> httpx.Client:
    global _sync_client
    if _sync_client is None:
        _sync_client = httpx.Client(
            timeout=httpx.Timeout(120.0, read=115.0),
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=50)
        )
    return _sync_client

# ── Intent keywords (REORDERED: specific first, general last) ─────────────────
_INTENTS = {
    "availability": [
        "còn bàn", "còn chỗ", "chỗ trống", "slot", "available",
        "đặt bàn", "book", "hết chỗ", "kiểm tra", "còn không",
        "còn trống", "bàn trống", "được không", "có chỗ"
    ],
    "times": [
        "giờ khác", "thời gian khác", "khung giờ khác", "giờ nào",
        "mấy giờ", "khung giờ", "thời gian", "lúc mấy giờ"
    ],
    "dates": [
        "ngày khác", "hôm khác", "ngày nào", "hôm nào", "ngày nào còn",
        "hôm nào còn", "ngày nào trống", "hôm nào trống",
        "ngày mai", "hôm nay", "ngày kia", "thứ mấy"
    ],
    "greeting": [
        "chào", "hi", "hello", "xin chào", "chào bạn", "chào bot",
        "chào buổi", "chào buổi sáng", "chào buổi tối",
        "hey", "có ai không", "giúp tôi"
    ],
    "recommend": [
        "ăn gì", "gợi ý", "restaurant", "recommend",
        "quán", "muốn ăn", "tìm quán", "đề xuất", "giới thiệu",
        "cho tôi xin", "nên ăn", "địa điểm", "món ngon"
    ],
}


def _detect_intent(text: str) -> str | None:
    """Phát hiện intent với logging"""
    lower = text.lower()
    for intent, keywords in _INTENTS.items():
        if any(kw in lower for kw in keywords):
            logger.info(f"✅ Intent detected: {intent} from text: {text[:50]}...")
            return intent
    logger.info(f"❌ No intent detected for text: {text[:50]}...")
    return None


def _get_greeting_response() -> str:
    import random
    greetings = [
        "Xin chào! Tôi có thể giúp gì cho bạn hôm nay? 🍽️",
        "Chào bạn! Bạn muốn tìm nhà hàng hay đặt bàn ạ?",
        "Hi! Tôi là trợ lý đặt bàn nhà hàng. Bạn cần tôi hỗ trợ gì không?"
    ]
    return random.choice(greetings)


async def _find_restaurant(name_hint: str, token: str) -> dict | None:
    if not token:
        logger.warning("Token is empty in _find_restaurant")
        return None
        
    try:
        client = await get_http_client()
        res = await client.get(
            f"{INTERNAL_BASE}/restaurants/",
            params={"search": name_hint, "limit": 5},
            headers={"Authorization": f"Bearer {token}"},
        )
        res.raise_for_status()
        
        data = res.json()
        if not isinstance(data, dict):
            logger.error(f"Unexpected response type: {type(data)}")
            return None
            
        items = data.get("data", [])
        if not isinstance(items, list):
            logger.error(f"Items is not a list: {type(items)}")
            return None

        if not items:
            logger.info(f"No restaurant found for hint: {name_hint}")
            return None

        hint_lower = name_hint.lower()
        for r in items:
            if hint_lower in r.get("name", "").lower():
                logger.info(f"Found restaurant: {r.get('name')}")
                return r
        logger.info(f"Using first restaurant: {items[0].get('name')}")
        return items[0]
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error finding restaurant: {e.response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Error finding restaurant: {e}", exc_info=True)
        return None


def _extract_restaurant_hint(text: str) -> str:
    """Trích xuất tên nhà hàng từ câu hỏi của user"""
    triggers = ["ở ", "tại ", "nhà hàng ", "quán ", "restaurant ", "cho "]
    lower = text.lower()
    for trig in triggers:
        idx = lower.find(trig)
        if idx != -1:
            after = text[idx + len(trig):].strip()
            for stop in ["không", "còn", "có", "?", ",", ".", "\n", " ạ"]:
                pos = after.lower().find(stop)
                if pos != -1:
                    after = after[:pos].strip()
            if after:
                logger.info(f"Extracted restaurant hint: {after}")
                return after
    
    # Fallback: lấy từ đầu tiên nếu không có trigger
    words = text.split()
    for word in words:
        if len(word) > 3 and word not in ["còn", "bàn", "không", "kiểm", "tra"]:
            logger.info(f"Fallback restaurant hint: {word}")
            return word
    return ""


async def _fetch_recommendations(token: str, db: AsyncSession, user_id: int) -> str:
    """Lấy danh sách nhà hàng gợi ý - gọi service trực tiếp"""
    if not token:
        logger.warning("Token is empty in _fetch_recommendations")
        return "⚠️ Vui lòng đăng nhập để xem gợi ý nhà hàng."
        
    try:
        # Gọi service trực tiếp không dùng HTTP
        items = await get_recommendations(
            db=db,
            user_id=user_id,
            limit=5,
            for_date=date.today()
        )
        
        if not items:
            return "⚠️ Hiện tại chưa có nhà hàng nào được gợi ý. Bạn có thể thử tìm theo tên nhà hàng cụ thể."

        lines = ["🍽️ Gợi ý nhà hàng dành cho bạn:\n"]
        for i, r in enumerate(items[:5], 1):
            # r là dict: { restaurant: Restaurant, score: float, reason: str, available_seats: int }
            restaurant_data = r.get("restaurant")
            if restaurant_data:
                name = restaurant_data.name or "Nhà hàng không rõ tên"
                cuisine = restaurant_data.cuisine_type or ""
            else:
                name = "Nhà hàng không rõ tên"
                cuisine = ""

            lines.append(f"{i}. {name}" + (f" ({cuisine})" if cuisine else ""))
        
        result = "\n".join(lines)
        logger.info(f"Recommendations fetched successfully: {len(items)} restaurants")
        return result
    except Exception as e:
        logger.error(f"Error fetching recommendations: {str(e)}", exc_info=True)
        return "⚠️ Hiện tại không thể lấy gợi ý nhà hàng. Vui lòng thử lại sau."


async def _fetch_availability(token: str, restaurant_id: int | None, restaurant_name: str, db: AsyncSession, user_id: int) -> str:
    """Kiểm tra tình trạng bàn"""
    if not token:
        return "⚠️ Vui lòng đăng nhập để kiểm tra chỗ trống."
        
    if not restaurant_id:
        logger.info("No restaurant_id provided for availability check")
        try:
            recs = await _fetch_recommendations(token, db, user_id)
            return f"Bạn muốn kiểm tra nhà hàng nào? Dưới đây là một số gợi ý:\n{recs}\nHãy cho tôi biết tên nhà hàng cụ thể nhé! 🍜"
        except Exception as e:
            logger.error(f"Error in availability fallback: {e}")
            return "⚠️ Vui lòng cho tôi biết tên nhà hàng bạn muốn kiểm tra chỗ trống."

    try:
        logger.info(f"Checking availability for restaurant_id={restaurant_id}")
        client = await get_http_client()
        res = await client.get(
            f"{INTERNAL_BASE}/suggestions/heatmap/{restaurant_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        res.raise_for_status()
        
        data = res.json()
        if not isinstance(data, dict):
            return "📊 Không thể lấy thông tin chi tiết, nhưng nhà hàng có thể còn bàn."
            
        name_label = f"**{restaurant_name}**" if restaurant_name else "nhà hàng này"
        result = f"📊 Tình trạng bàn tại {name_label}: {data.get('summary', 'Có bàn trống.')}"
        logger.info(f"Availability result: {result}")
        return result
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error checking availability: {e.response.status_code}")
        if e.response.status_code == 404:
            return "⚠️ Không tìm thấy thông tin nhà hàng này."
        return "⚠️ Hiện tại không thể kiểm tra chỗ trống, vui lòng thử lại sau."
    except Exception as e:
        logger.error(f"Error checking availability: {e}", exc_info=True)
        return "⚠️ Hiện tại không thể kiểm tra chỗ trống, vui lòng thử lại sau."


async def _fetch_times(token: str, params: dict) -> str:
    """Lấy gợi ý khung giờ"""
    if not token:
        return "⚠️ Vui lòng đăng nhập để xem giờ đặt bàn."
        
    if not params.get("restaurant_id"):
        return "🕐 Bạn muốn xem giờ đặt bàn cho nhà hàng nào? Hãy cho tôi biết tên nhà hàng để tôi hỗ trợ tốt hơn nhé!"

    try:
        logger.info(f"Fetching times with params: {params}")
        client = await get_http_client()
        res = await client.get(
            f"{INTERNAL_BASE}/suggestions/times",
            params=params,
            headers={"Authorization": f"Bearer {token}"},
        )
        res.raise_for_status()
        
        data = res.json()
        items = data if isinstance(data, list) else data.get("data", []) if isinstance(data, dict) else []

        if not items:
            return "⚠️ Không có khung giờ thay thế nào còn chỗ."

        lines = ["🕐 Các khung giờ còn chỗ:\n"]
        for s in items[:5]:
            t = str(s.get("booking_time", ""))[:5]
            avail = s.get("available", "?")
            lines.append(f"• {t} — còn {avail} chỗ")
        return "\n".join(lines)
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching times: {e.response.status_code}")
        return "⚠️ Hiện tại không thể lấy gợi ý giờ đặt bàn."
    except Exception as e:
        logger.error(f"Error fetching times: {e}", exc_info=True)
        return "⚠️ Hiện tại không thể lấy gợi ý giờ đặt bàn."


async def _fetch_dates(token: str, params: dict) -> str:
    """Lấy gợi ý ngày"""
    if not token:
        return "⚠️ Vui lòng đăng nhập để xem ngày đặt bàn."
        
    if not params.get("restaurant_id"):
        return "📅 Bạn muốn xem ngày đặt bàn cho nhà hàng nào? Hãy cho tôi biết tên nhà hàng để tôi hỗ trợ nhé!"

    try:
        logger.info(f"Fetching dates with params: {params}")
        client = await get_http_client()
        res = await client.get(
            f"{INTERNAL_BASE}/suggestions/dates",
            params=params,
            headers={"Authorization": f"Bearer {token}"},
        )
        res.raise_for_status()
        
        data = res.json()
        items = data if isinstance(data, list) else data.get("data", []) if isinstance(data, dict) else []

        if not items:
            return "⚠️ Không tìm thấy ngày thay thế nào còn chỗ."

        lines = ["📅 Các ngày còn chỗ gần nhất:\n"]
        for s in items[:5]:
            d = s.get("booking_date", "")
            avail = s.get("available", "?")
            lines.append(f"• {d} — còn {avail} chỗ")
        return "\n".join(lines)
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching dates: {e.response.status_code}")
        return "⚠️ Hiện tại không thể lấy gợi ý ngày đặt bàn."
    except Exception as e:
        logger.error(f"Error fetching dates: {e}", exc_info=True)
        return "⚠️ Hiện tại không thể lấy gợi ý ngày đặt bàn."


# ========== THÊM MỚI: API /suggestions/slot ==========
async def _fetch_slot(token: str, params: dict) -> str:
    """
    Check slot - Gọi API /api/v1/suggestions/slot
    API này kiểm tra khung giờ đặt bàn còn trống
    """
    if not token:
        return "⚠️ Vui lòng đăng nhập để kiểm tra slot."
        
    if not params.get("restaurant_id"):
        return "⏰ Bạn muốn kiểm tra slot cho nhà hàng nào? Hãy cho tôi biết tên nhà hàng cụ thể nhé!"

    try:
        logger.info(f"Checking slot with params: {params}")
        client = await get_http_client()
        res = await client.get(
            f"{INTERNAL_BASE}/suggestions/slot",  # API endpoint
            params=params,
            headers={"Authorization": f"Bearer {token}"},
        )
        res.raise_for_status()
        
        data = res.json()
        
        # Xử lý response data
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = data.get("data", [])
        else:
            items = []
        
        if not items:
            return "⏰ Hiện tại không có slot trống cho nhà hàng này."
        
        lines = ["⏰ Các slot còn trống:\n"]
        for s in items[:5]:
            time_slot = s.get("time") or s.get("booking_time") or s.get("slot_time", "")
            available = s.get("available") or s.get("slots_available") or s.get("capacity", "?")
            lines.append(f"• {time_slot} — còn {available} chỗ")
        
        return "\n".join(lines)
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error checking slot: {e.response.status_code}")
        if e.response.status_code == 404:
            return "⚠️ API check slot không khả dụng. Vui lòng thử lại sau."
        return "⚠️ Hiện tại không thể kiểm tra slot, vui lòng thử lại sau."
    except Exception as e:
        logger.error(f"Error checking slot: {e}", exc_info=True)
        return "⚠️ Hiện tại không thể kiểm tra slot, vui lòng thử lại sau."


def _call_ollama_sync(prompt: str, context: str = "") -> str:
    """Gọi Ollama sync"""
    try:
        full_prompt = prompt
        if context:
            full_prompt = f"{context}\n\nNgười dùng: {prompt}\nTrợ lý:"
        
        logger.debug(f"[OLLAMA] Sending prompt to {OLLAMA_URL}, model={OLLAMA_MODEL}")
        
        client = get_sync_client()
        response = client.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": full_prompt, "stream": False},
        )
        response.raise_for_status()
        result = response.json()
        
        reply = result.get("response", "").strip()
        logger.debug(f"[OLLAMA] Response received, length={len(reply)}, keys={list(result.keys())}")
        
        # ✅ Kiểm tra response rỗng
        if not reply:
            logger.warning(f"[OLLAMA] Empty response from Ollama. Full response: {result}")
            return "⚠️ Xin lỗi, tôi không có phản hồi phù hợp. Vui lòng thử hỏi khác."
        
        return reply
    except httpx.HTTPStatusError as e:
        logger.error(f"[OLLAMA] HTTP error: {e.response.status_code} - {e.response.text}")
        return "⚠️ Hiện tại không thể kết nối đến AI. Vui lòng thử lại sau."
    except Exception as e:
        logger.error(f"[OLLAMA] Error: {e}", exc_info=True)
        return "⚠️ Có lỗi xảy ra khi xử lý tin nhắn của bạn."


def _build_context(messages: list[dict]) -> str:
    """Xây dựng context từ lịch sử chat"""
    context_lines = []
    for msg in messages[-5:]:  # Lấy 5 tin nhắn gần nhất
        role = "Người dùng" if msg.get("role") == "user" else "Trợ lý"
        content = msg.get("content", "")
        context_lines.append(f"{role}: {content}")
    context = "\n".join(context_lines)
    logger.info(f"Built context with {len(context_lines)} messages")
    return context


async def process_chat_message(
    messages: list[dict],
    db: AsyncSession,
    user_id: int,
    token: str = "",
) -> dict:
    """
    Xử lý tin nhắn chat - MAIN FUNCTION
    """
    logger.info(f"=" * 50)
    logger.info(f"Processing message for user_id={user_id}, token exists={bool(token)}")
    
    # Lấy tin nhắn cuối cùng của user
    user_message = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            user_message = m.get("content", "")
            break

    if not user_message:
        logger.warning("Empty user message received")
        return {"reply": "Vui lòng nhập tin nhắn.", "intent": None}

    logger.info(f"User message: {user_message}")
    
    # Detect intent
    intent = _detect_intent(user_message)
    logger.info(f"Detected intent: {intent}")
    
    # Kiểm tra token cho các intent cần gọi API
    requires_auth_intents = ["recommend", "availability", "times", "dates", "slot"]
    
    if intent in requires_auth_intents and not token:
        logger.warning(f"Missing token for intent: {intent}")
        return {"reply": "⚠️ Vui lòng đăng nhập để sử dụng tính năng này.", "intent": intent}

    # Xử lý greeting
    if intent == "greeting":
        reply = _get_greeting_response()
        logger.info(f"Greeting response: {reply[:50]}...")
        return {"reply": reply, "intent": intent}

    # Xử lý recommend
    if intent == "recommend":
        logger.info("🔄 Processing RECOMMEND intent...")
        try:
            reply = await _fetch_recommendations(token, db, user_id)
            logger.info(f"✅ Recommend response: {reply[:100]}...")
        except Exception as e:
            logger.error(f"Error in recommend intent: {e}", exc_info=True)
            reply = "⚠️ Hiện tại không thể lấy danh sách nhà hàng."
        return {"reply": reply, "intent": intent}

    # Xử lý availability
    if intent == "availability":
        logger.info("🔄 Processing AVAILABILITY intent...")
        name_hint = _extract_restaurant_hint(user_message)
        restaurant_id = None
        restaurant_name = name_hint

        if name_hint:
            logger.info(f"Looking for restaurant: {name_hint}")
            try:
                rest = await _find_restaurant(name_hint, token)
                if rest and isinstance(rest, dict):
                    restaurant_id = rest.get("id")
                    restaurant_name = rest.get("name", name_hint)
                    logger.info(f"Found restaurant: id={restaurant_id}, name={restaurant_name}")
            except Exception as e:
                logger.error(f"Error finding restaurant for availability: {e}")

        reply = await _fetch_availability(token, restaurant_id, restaurant_name, db, user_id)
        logger.info(f"✅ Availability response: {reply[:100]}...")
        return {"reply": reply, "intent": intent}

    # Xử lý times
    if intent == "times":
        logger.info("🔄 Processing TIMES intent...")
        name_hint = _extract_restaurant_hint(user_message)
        restaurant_id = None
        if name_hint:
            logger.info(f"Looking for restaurant: {name_hint}")
            try:
                rest = await _find_restaurant(name_hint, token)
                if rest and isinstance(rest, dict):
                    restaurant_id = rest.get("id")
                    logger.info(f"Found restaurant id={restaurant_id}")
            except Exception as e:
                logger.error(f"Error finding restaurant for times: {e}")

        params = {
            "restaurant_id": restaurant_id,
            "booking_date": date.today().isoformat(),
            "booking_time": datetime.now().time().strftime("%H:%M"),
            "guests": 2
        }
        reply = await _fetch_times(token, params)
        logger.info(f"✅ Times response: {reply[:100]}...")
        return {"reply": reply, "intent": intent}

    # Xử lý dates
    if intent == "dates":
        logger.info("🔄 Processing DATES intent...")
        name_hint = _extract_restaurant_hint(user_message)
        restaurant_id = None
        if name_hint:
            logger.info(f"Looking for restaurant: {name_hint}")
            try:
                rest = await _find_restaurant(name_hint, token)
                if rest and isinstance(rest, dict):
                    restaurant_id = rest.get("id")
                    logger.info(f"Found restaurant id={restaurant_id}")
            except Exception as e:
                logger.error(f"Error finding restaurant for dates: {e}")

        params = {
            "restaurant_id": restaurant_id,
            "booking_date": date.today().isoformat(),
            "preferred_time": datetime.now().time().strftime("%H:%M"),
            "guests": 2
        }
        reply = await _fetch_dates(token, params)
        logger.info(f"✅ Dates response: {reply[:100]}...")
        return {"reply": reply, "intent": intent}

    # ========== THÊM MỚI: Xử lý slot ==========
    if intent == "slot":
        logger.info("🔄 Processing SLOT intent...")
        name_hint = _extract_restaurant_hint(user_message)
        restaurant_id = None
        if name_hint:
            logger.info(f"Looking for restaurant: {name_hint}")
            try:
                rest = await _find_restaurant(name_hint, token)
                if rest and isinstance(rest, dict):
                    restaurant_id = rest.get("id")
                    logger.info(f"Found restaurant id={restaurant_id}")
            except Exception as e:
                logger.error(f"Error finding restaurant for slot: {e}")

        params = {
            "restaurant_id": restaurant_id,
            "date": date.today().isoformat(),
            "guests": 2
        }
        reply = await _fetch_slot(token, params)
        logger.info(f"✅ Slot response: {reply[:100]}...")
        return {"reply": reply, "intent": intent}

    # General conversation → Ollama
    logger.info("🔄 No specific intent matched, falling back to Ollama...")
    try:
        # Lấy context từ lịch sử chat (bao gồm cả tin nhắn hiện tại)
        context = _build_context(messages)
        loop = asyncio.get_running_loop()
        reply = await loop.run_in_executor(
            None, 
            partial(_call_ollama_sync, user_message, context)
        )
        
        # ✅ Final validation - ensure reply is not empty
        if not reply or not reply.strip():
            logger.error(f"[CRITICAL] Ollama returned empty reply!")
            reply = "⚠️ Xin lỗi, tôi không có phản hồi phù hợp lúc này. Vui lòng thử hỏi khác."
        else:
            logger.info(f"✅ Ollama response: {reply[:100]}...")
    except Exception as e:
        logger.error(f"Error calling Ollama: {e}", exc_info=True)
        reply = "⚠️ Xin lỗi, tôi đang gặp chút vấn đề kỹ thuật. Vui lòng thử lại sau."
    
    return {"reply": reply, "intent": intent}


async def cleanup_clients():
    global _http_client, _sync_client
    if _http_client and not _http_client.is_closed:
        await _http_client.aclose()
    if _sync_client:
        _sync_client.close()