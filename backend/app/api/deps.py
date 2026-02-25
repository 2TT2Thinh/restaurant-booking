from typing import AsyncGenerator
from app.db.session import AsyncSessionLocal # Đảm bảo đúng tên này

async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session