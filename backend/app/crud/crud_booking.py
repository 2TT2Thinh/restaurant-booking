from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate


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

async def update_booking(db: AsyncSession, booking_id: int, obj_in: BookingUpdate, user_id: int):
    # 1. Tìm đơn đặt bàn
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id, Booking.user_id == user_id)
    )
    db_obj = result.scalars().first()
    
    if not db_obj:
        return None # Không tìm thấy hoặc không có quyền sửa

    # 2. Cập nhật các trường dữ liệu được gửi lên
    update_data = obj_in.model_dump(exclude_unset=True) # Chỉ lấy các trường user có nhập
    for field in update_data:
        setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_booking(db: AsyncSession, booking_id: int, user_id: int):
    # 1. Tìm đơn đặt bàn thỏa mãn cả ID và User_ID
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id, Booking.user_id == user_id)
    )
    db_obj = result.scalars().first()
    
    if not db_obj:
        return None # Không tìm thấy hoặc không có quyền xóa

    # 2. Thực hiện xóa vĩnh viễn khỏi Database
    await db.delete(db_obj)
    await db.commit()
    return db_obj



async def get_multi_bookings(
    db: AsyncSession, 
    user_id: int, 
    search: Optional[str] = None, 
    status: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[Booking]:
    # 1. Khởi tạo câu lệnh query cơ bản (Lọc theo chủ sở hữu trước)
    query = select(Booking).where(Booking.user_id == user_id)

    # 2. Xử lý tìm kiếm (Search)
    if search:
        # trim() và loại bỏ khoảng trắng thừa để search chính xác hơn
        search_term = f"%{search.strip()}%"
        # ilike tìm không phân biệt hoa thường
        query = query.where(Booking.restaurant_name.ilike(search_term))

    # 3. Xử lý lọc theo trạng thái (Filter)
    # Status != "all" giúp trả về tất cả nếu người dùng nhấn vào Tab "Tất cả"
    if status and status.lower() != "all":
        query = query.where(Booking.status == status.lower())

    # 4. Sắp xếp (Audit Timestamps): Mới nhất lên đầu
    # Sau đó mới thực hiện phân trang (offset/limit)
    query = query.order_by(Booking.created_at.desc())
    query = query.offset(skip).limit(limit)
    
    # 5. Thực thi
    result = await db.execute(query)
    return result.scalars().all()