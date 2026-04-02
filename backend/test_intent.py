#!/usr/bin/env python3
"""
Test intent detection
"""
from app.services.chatbot_service import _detect_intent

# Test intent detection
test_messages = [
    'gợi ý nhà hàng',
    'nhà hàng ABC còn bàn không',
    'nhà hàng ABC giờ nào còn',
    'nhà hàng ABC ngày nào còn',
    'xin chào',
    'bạn có thể giúp gì',
    'tôi muốn đặt bàn'
]

print('🔍 Testing intent detection:')
for msg in test_messages:
    intent = _detect_intent(msg)
    print(f'"{msg}" -> {intent}')