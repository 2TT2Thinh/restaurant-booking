#!/usr/bin/env python3
"""
Debug script để kiểm tra chatbot service
Chạy lệnh: python test_chatbot_debug.py
"""
import asyncio
import logging
from app.services.chatbot_service import process_chat_message, _call_ollama_sync
from app.core.config import settings

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_ollama_directly():
    """Test Ollama connection directly"""
    print("\n" + "="*60)
    print("TEST 1: Direct Ollama Connection")
    print("="*60)
    try:
        reply = _call_ollama_sync("Xin chào, bạn là ai?", "")
        print(f"✅ Ollama reply: {reply}")
        print(f"   Length: {len(reply)} chars")
        print(f"   Empty: {not reply or not reply.strip()}")
        return reply
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def test_chatbot_service():
    """Test chatbot service with greeting"""
    print("\n" + "="*60)
    print("TEST 2: Chatbot Greeting")
    print("="*60)
    try:
        messages = [{"role": "user", "content": "Xin chào"}]
        result = await process_chat_message(
            messages=messages,
            db=None,
            user_id=1,
            token=""
        )
        print(f"✅ Service reply: {result.get('reply')}")
        print(f"   Intent: {result.get('intent')}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def test_chatbot_service_general():
    """Test chatbot service with general message"""
    print("\n" + "="*60)
    print("TEST 3: Chatbot General Conversation")
    print("="*60)
    try:
        messages = [
            {"role": "user", "content": "Bạn có thể giúp tôi gì?"}
        ]
        result = await process_chat_message(
            messages=messages,
            db=None,
            user_id=1,
            token=""
        )
        reply = result.get('reply', '')
        print(f"✅ Service reply: {reply}")
        print(f"   Intent: {result.get('intent')}")
        print(f"   Length: {len(reply)} chars")
        print(f"   Empty: {not reply or not reply.strip()}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    print(f"\n🔍 Chatbot Debug Tests")
    print(f"OLLAMA_HOST: {settings.OLLAMA_HOST}")
    print(f"OLLAMA_MODEL_NAME: {settings.OLLAMA_MODEL_NAME}")
    print(f"INTERNAL_BASE_URL: {settings.INTERNAL_BASE_URL}")
    
    # Run tests
    result1 = await test_ollama_directly()
    result2 = await test_chatbot_service()
    result3 = await test_chatbot_service_general()
    
    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    print(f"1. Direct Ollama: {'✅ OK' if result1 and result1.strip() else '❌ FAIL'}")
    print(f"2. Greeting: {'✅ OK' if result2 and result2.get('reply') else '❌ FAIL'}")
    print(f"3. General Conv: {'✅ OK' if result3 and result3.get('reply') and result3.get('reply').strip() else '❌ FAIL'}")

if __name__ == "__main__":
    asyncio.run(main())
