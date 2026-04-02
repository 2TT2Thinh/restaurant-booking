# app/api/v1/endpoints/chatbot.py
import time
import logging
import asyncio
from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field, validator

from app.api import deps
from app.core.config import settings
from app.models.user import User
from app.services.chatbot_service import process_chat_message

logger = logging.getLogger(__name__)
router = APIRouter()

# Constants
MAX_MESSAGE_LENGTH = 2000
MAX_MESSAGES = 20
MIN_MESSAGES = 1

class MessageRole(str, Enum):
    """Allowed message roles"""
    USER = "user"
    ASSISTANT = "assistant"

class ChatMessage(BaseModel):
    """Single chat message"""
    role: MessageRole
    content: str = Field(..., min_length=1, max_length=MAX_MESSAGE_LENGTH)
    
    @validator('content')
    def validate_content(cls, v):
        """Additional content validation"""
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty or whitespace only")
        return v.strip()

class ChatRequest(BaseModel):
    """Chat request model"""
    messages: list[ChatMessage] = Field(
        ..., 
        min_length=MIN_MESSAGES, 
        max_length=MAX_MESSAGES
    )
    
    @validator('messages')
    def validate_messages(cls, v):
        """Validate message sequence"""
        # Check last message is from user
        if v and v[-1].role != MessageRole.USER:
            raise ValueError("Last message must be from user")
        
        # Check alternating roles (optional but good practice)
        for i in range(1, len(v)):
            if v[i].role == v[i-1].role:
                # Allow consecutive same roles (for system prompts), but warn
                logger.warning(f"Consecutive messages with same role: {v[i].role}")
        
        return v

class ChatResponse(BaseModel):
    """Chat response model - CLEAN VERSION (no duplicate data)"""
    data: str  # ✅ Chỉ 1 field data cho frontend
    intent: Optional[str] = None
    processing_time_ms: int = 0

@router.post(
    "/", 
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with restaurant booking assistant",
    description="Send a message to the AI assistant for restaurant recommendations and booking"
)
async def chat(
    request: Request,
    body: ChatRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Chat endpoint with proper error handling and logging
    """
    start_time = time.time()
    
    # Extract and validate token
    auth_header = request.headers.get("Authorization", "")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning(f"Missing or invalid auth header from user {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        logger.warning(f"Empty token from user {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token cannot be empty"
        )
    
    # Log request
    logger.info(
        f"Chat request from user {current_user.id}, "
        f"messages={len(body.messages)}, "
        f"last_message_len={len(body.messages[-1].content)}"
    )
    
    # Convert to dict format for service
    messages_dict = [
        {"role": m.role.value, "content": m.content} 
        for m in body.messages
    ]
    
    try:
        # Process message with timeout protection
        result = await process_chat_message(
            messages=messages_dict,
            db=db,
            user_id=current_user.id,
            token=token,
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        reply_text = result.get("reply", "⚠️ Không có phản hồi từ server.")
        intent_detected = result.get("intent")
        
        # ✅ Final validation - ensure reply is never empty
        if not reply_text or not reply_text.strip():
            logger.error(f"[CRITICAL] Empty reply detected for user {current_user.id}! Result: {result}")
            reply_text = "⚠️ Xin lỗi, có lỗi xảy ra. Vui lòng thử lại sau."
        
        # Log response for debugging
        logger.info(
            f"Chat response for user {current_user.id}: "
            f"intent={intent_detected}, "
            f"processing_time={processing_time}ms, "
            f"reply_len={len(reply_text)}"
        )
        
        # ✅ Clean response - only data field for frontend
        return ChatResponse(
            data=reply_text,
            intent=intent_detected,
            processing_time_ms=processing_time
        )
        
    except asyncio.TimeoutError:
        logger.error(f"Timeout processing chat for user {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request processing timeout. Please try again."
        )
    except Exception as e:
        logger.error(
            f"Error processing chat for user {current_user.id}: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your message. Please try again later."
        )


# Optional: Add health check endpoint
@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint for chatbot service"""
    return {"status": "healthy", "service": "chatbot"}


# Optional: Add endpoint to get supported intents
@router.get("/intents", response_model=dict)
async def get_intents():
    """Get list of supported intents (for client-side optimization)"""
    return {
        "intents": ["recommend", "availability", "times", "dates", "greeting"],
        "description": "Intent detection is automatic based on message content"
    }