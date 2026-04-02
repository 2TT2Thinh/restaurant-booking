from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, or_, and_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, timezone

from app.api import deps
from app.models.user import User
from app.models.booking import Booking
from app.models.restaurant import Restaurant
from app.schemas.booking import BookingRead, BookingUpdate
from app.schemas.user import UserRead
from app.schemas.response import DataResponse
from pydantic import BaseModel

router = APIRouter()

# ==================== SCHEMAS RIÊNG CHO ADMIN ====================

class AdminUserUpdate(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[str] = None  # "customer" | "admin"

class AdminBookingUpdate(BaseModel):
    status: str  # "confirmed" | "cancelled" | "pending"

# ==================== STATS TỔNG QUAN ====================

@router.get("/stats")
async def get_admin_stats(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    """Thống kê tổng quan cho Admin Dashboard"""

    # Tổng số booking
    total_bookings = await db.scalar(select(func.count(Booking.id)))

    # Booking theo status
    booking_stats = await db.execute(
        select(
            func.count(case((Booking.status == "pending",   1))).label("pending"),
            func.count(case((Booking.status == "confirmed", 1))).label("confirmed"),
            func.count(case((Booking.status == "cancelled", 1))).label("cancelled"),
        )
    )
    brow = booking_stats.one()

    # Tổng số nhà hàng
    total_restaurants = await db.scalar(select(func.count(Restaurant.id)))

    # Tổng số user
    total_users = await db.scalar(select(func.count(User.id)))

    # User active
    active_users = await db.scalar(
        select(func.count(User.id)).where(User.is_active == True)
    )

    return {
        "total_bookings":    total_bookings   or 0,
        "pending_bookings":  brow.pending     or 0,
        "confirmed_bookings": brow.confirmed  or 0,
        "cancelled_bookings": brow.cancelled  or 0,
        "total_restaurants": total_restaurants or 0,
        "total_users":       total_users      or 0,
        "active_users":      active_users     or 0,
    }

# ==================== QUẢN LÝ BOOKING ====================

@router.get("/bookings", response_model=DataResponse[List[BookingRead]])
async def get_all_bookings(
    search: Optional[str] = None,
    status: Optional[str] = None,
    restaurant_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    """Lấy tất cả booking của mọi user"""
    query = (
        select(Booking)
        .options(selectinload(Booking.restaurant))
        .options(selectinload(Booking.user))
    )

    if search:
        query = query.join(Restaurant).where(
            Restaurant.name.ilike(f"%{search.strip()}%")
        )

    if status and status.lower() != "all":
        query = query.where(Booking.status == status.lower())

    if restaurant_id:
        query = query.where(Booking.restaurant_id == restaurant_id)

    query = query.order_by(Booking.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    bookings = result.scalars().all()
    return DataResponse.create(bookings)


@router.patch("/bookings/{booking_id}", response_model=BookingRead)
async def admin_update_booking(
    booking_id: int,
    obj_in: AdminBookingUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    """Admin xác nhận hoặc hủy bất kỳ booking nào"""
    if obj_in.status not in ["pending", "confirmed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Status không hợp lệ")

    result = await db.execute(
        select(Booking)
        .options(selectinload(Booking.restaurant))
        .where(Booking.id == booking_id)
    )
    booking = result.scalars().first()

    if not booking:
        raise HTTPException(status_code=404, detail="Không tìm thấy booking")

    booking.status = obj_in.status
    db.add(booking)
    await db.commit()

    result = await db.execute(
        select(Booking)
        .options(selectinload(Booking.restaurant))
        .where(Booking.id == booking_id)
    )
    return result.scalars().first()


@router.delete("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_booking(
    booking_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    """Admin xóa bất kỳ booking nào"""
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Không tìm thấy booking")
    await db.delete(booking)
    await db.commit()
    return None

# ==================== QUẢN LÝ USER ====================

@router.get("/users", response_model=DataResponse[List[UserRead]])
async def get_all_users(
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    """Lấy danh sách tất cả user"""
    query = select(User)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.where(
            or_(
                User.full_name.ilike(search_term),
                User.email.ilike(search_term)
            )
        )

    if is_active is not None:
        query = query.where(User.is_active == is_active)

    query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    return DataResponse.create(users)


@router.patch("/users/{user_id}", response_model=UserRead)
async def admin_update_user(
    user_id: int,
    obj_in: AdminUserUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    """Admin đổi role hoặc kích hoạt/vô hiệu hóa user"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy user")

    # Không cho admin tự đổi role chính mình
    if user.id == current_user.id and obj_in.role == "customer":
        raise HTTPException(
            status_code=400,
            detail="Không thể tự hạ quyền chính mình!"
        )

    if obj_in.is_active is not None:
        user.is_active = obj_in.is_active
    if obj_in.role is not None:
        if obj_in.role not in ["customer", "admin"]:
            raise HTTPException(status_code=400, detail="Role không hợp lệ")
        user.role = obj_in.role

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user