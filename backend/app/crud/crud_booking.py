from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.booking import Booking

async def get_user_bookings(db: AsyncSession, user_id: int):
    # 1. Tạo câu lệnh select (SQLAlchemy 2.0 style)
    query = select(Booking).where(Booking.user_id == user_id).order_by(Booking.created_at.desc())
    
    # 2. THỰC THI: Bắt buộc phải có await ở đây
    result = await db.execute(query)
    
    # 3. TRẢ VỀ: scalars() giúp lấy ra danh sách object Booking sạch sẽ
    return result.scalars().all()