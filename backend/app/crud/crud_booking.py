from typing import List, Optional
from datetime import datetime,timezone, timedelta
from sqlalchemy import func, or_, select, and_, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate
from app.core.config import settings
from sqlalchemy.orm import selectinload
from app.models.restaurant import Restaurant
from fastapi import HTTPException

async def get_user_bookings(db: AsyncSession, user_id: int):
    query = (
        select(Booking)
        .options(selectinload(Booking.restaurant))  # THÊM dòng này
        .where(Booking.user_id == user_id)
        .order_by(Booking.created_at.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()

# Hàm tạo lưu vào database một booking mới, nhận vào dữ liệu từ BookingCreate và user_id để gán cho booking đó
async def create_booking(db: AsyncSession, obj_in: BookingCreate, user_id: int):
    # THÊM: Check nhà hàng tồn tại
    restaurant = await db.get(Restaurant, obj_in.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")

    # THÊM: Check số khách không vượt capacity
    if obj_in.number_of_guests > restaurant.max_capacity:
        raise HTTPException(
            status_code=400,
            detail=f"Nhà hàng chỉ chứa tối đa {restaurant.max_capacity} khách"
        )

    # THÊM: Check trùng giờ
    conflict = await db.execute(
        select(Booking).where(
            Booking.restaurant_id == obj_in.restaurant_id,
            Booking.booking_date == obj_in.booking_date,
            Booking.booking_time == obj_in.booking_time,
            Booking.status != "cancelled"
        )
    )
    if conflict.scalars().first():
        raise HTTPException(status_code=400, detail="Khung giờ này đã có người đặt")

    # GIỮ NGUYÊN phần tạo booking
    new_booking = Booking(
        **obj_in.model_dump(),
        user_id=user_id,
        status="pending"
    )
    db.add(new_booking)
    await db.commit()
    
    # Query lại với selectinload để load restaurant relationship
    result = await db.execute(
        select(Booking)
        .options(selectinload(Booking.restaurant))
        .where(Booking.id == new_booking.id)
    )
    return result.scalars().first()

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

    result = await db.execute(
        select(Booking)
        .options(selectinload(Booking.restaurant))
        .where(Booking.id == db_obj.id)
    )
    return result.scalars().first()


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
    # THÊM selectinload để load restaurant info cùng lúc, tránh query N+1
    query = (
        select(Booking)
        .options(selectinload(Booking.restaurant))
        .where(Booking.user_id == user_id)
    )

    if search:
        search_term = f"%{search.strip()}%"
        # SỬA: JOIN Restaurant thay vì search Booking.restaurant_name
        query = query.join(Restaurant).where(
            Restaurant.name.ilike(search_term)
        )

    # GIỮ NGUYÊN phần status, order, offset, limit
    if status and status.lower() != "all":
        query = query.where(Booking.status == status.lower())

    query = query.order_by(Booking.created_at.desc())
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

#  ========================================== profile user
async def get_booking_stats(db: AsyncSession, user_id: int):
    # 1. Lấy thời gian hiện tại
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    current_date = now_utc.date()
    current_time = now_utc.time() # Lấy riêng phần Giờ:Phút:Giây

    # 2. Query
    query = (
        select(
            func.count(Booking.id).label("total"),
            func.count(case((Booking.status == "confirmed", 1))).label("confirmed"),
            func.count(case((Booking.status == "cancelled", 1))).label("cancelled"),
            # Pending: status='pending' VÀ (Ngày > hôm nay HOẶC (Ngày == hôm nay VÀ Giờ >= bây giờ))
            func.count(case((
                and_(
                    Booking.status == "pending",
                    or_(
                        Booking.booking_date > current_date,
                        and_(Booking.booking_date == current_date, Booking.booking_time >= current_time)
                    )
                ), 1
            ))).label("pending"),
            # Expired: status='pending' VÀ (Ngày < hôm nay HOẶC (Ngày == hôm nay VÀ Giờ < bây giờ))
            func.count(case((
                and_(
                    Booking.status == "pending",
                    or_(
                        Booking.booking_date < current_date,
                        and_(Booking.booking_date == current_date, Booking.booking_time < current_time)
                    )
                ), 1
            ))).label("expired")
        )
        .where(Booking.user_id == user_id)
    )

    result = await db.execute(query)
    row = result.one()

    return {
        "total": row.total or 0,
        "confirmed": row.confirmed or 0,
        "cancelled": row.cancelled or 0,
        "pending": row.pending or 0,
        "expired": row.expired or 0
    }