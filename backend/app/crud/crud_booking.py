from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.booking import Booking
from app.schemas.booking import BookingCreate


async def get_user_bookings(db: AsyncSession, user_id: int):
    # 1. Tạo câu lệnh select (SQLAlchemy 2.0 style)
    query = select(Booking).where(Booking.user_id == user_id).order_by(Booking.created_at.desc())
    
    # 2. THỰC THI: Bắt buộc phải có await ở đây
    result = await db.execute(query)
    
    # 3. TRẢ VỀ: scalars() giúp lấy ra danh sách object Booking sạch sẽ
    return result.scalars().all()

# Hàm tạo lưu vào database một booking mới, nhận vào dữ liệu từ BookingCreate và user_id để gán cho booking đó
async def create_booking(db: AsyncSession, obj_in: BookingCreate, user_id: int):
    # Chuyển dữ liệu từ Pydantic Schema sang SQLAlchemy Model
    new_booking = Booking(
        **obj_in.model_dump(), # Lấy hết data từ Schema
        user_id=user_id,       # Tự động gán ID của người đang đăng nhập
        status="pending"       # Mặc định là đang chờ
    )
    
    db.add(new_booking)
    await db.commit()          # Lưu vào DB
    await db.refresh(new_booking) # Lấy lại ID và các trường tự động tạo
    return new_booking
