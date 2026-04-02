#!/usr/bin/env python3
"""
Test chatbot với empty token
"""
import asyncio
from app.services.chatbot_service import process_chat_message

async def test_with_mock_token():
    print('🔍 Testing chatbot with empty token...')

    # Empty token để test fallback
    fake_token = ''

    test_cases = [
        ('gợi ý nhà hàng', 'recommend'),
        ('nhà hàng ABC còn bàn không', 'availability'),
        ('nhà hàng ABC giờ nào còn', 'times'),
        ('nhà hàng ABC ngày nào còn', 'dates'),
        ('xin chào', 'greeting'),
        ('bạn có thể giúp gì', None)
    ]

    for message, expected_intent in test_cases:
        print(f'\n--- Testing: "{message}" ---')
        messages = [{'role': 'user', 'content': message}]
        result = await process_chat_message(messages, None, 1, fake_token)

        detected_intent = result.get('intent')
        reply = result.get('reply', '')[:100]

        status = '✅' if detected_intent == expected_intent else '❌'
        print(f'{status} Intent: {detected_intent} (expected: {expected_intent})')
        print(f'Reply: {reply}...')

if __name__ == "__main__":
    asyncio.run(test_with_mock_token())