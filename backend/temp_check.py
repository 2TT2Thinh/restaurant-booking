import asyncio
from app.services.chatbot_service import process_chat_message
from app.db.session import AsyncSession

async def run():
    async with AsyncSession() as session:
        res = await process_chat_message(
            messages=[{'role':'user', 'content':'gợi ý nhà hàng'}],
            db=session,
            user_id=1,
            token='fake-token'
        )
        print(res)

asyncio.run(run())