# app/api/v1/endpoints/bookings.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.api import deps
from app.crud import crud_booking
from app.schemas.booking import BookingCreate, BookingRead, BookingUpdate
from app.models.user import User
from app.exceptions import (
    BookingNotFound,
    CapacityExceeded,
    RestaurantNotFound,
    TimeSlotConflict,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# Helper: map domain exceptions → HTTP responses (single place, reused below)
# ---------------------------------------------------------------------------

def _handle_booking_domain_error(exc: Exception) -> None:
    if isinstance(exc, RestaurantNotFound):
        raise HTTPException(status_code=404, detail="Nhà hàng không tồn tại")
    if isinstance(exc, TimeSlotConflict):
        raise HTTPException(status_code=409, detail="Khung giờ này đã kín chỗ")
    if isinstance(exc, CapacityExceeded):
        raise HTTPException(
            status_code=400,
            detail=f"Nhà hàng không đủ chỗ. Còn trống: {exc.available} khách",
        )
    if isinstance(exc, BookingNotFound):
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đơn đặt bàn hoặc bạn không có quyền chỉnh sửa",
        )
    raise exc  # unexpected — let FastAPI's default 500 handler take it


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/stats")
async def get_my_stats(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Thống kê booking cho trang Profile và Dashboard"""
    return await crud_booking.get_booking_stats(db, user_id=current_user.id)


@router.get("/me", response_model=List[BookingRead])
async def read_my_bookings(
    search: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, le=100),
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return await crud_booking.get_multi_bookings(
        db=db,
        user_id=current_user.id,
        search=search,
        status=status,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def create_new_booking(
    booking_in: BookingCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Tạo đơn đặt bàn mới.
    - Kiểm tra nhà hàng tồn tại
    - Kiểm tra sức chứa trong khung giờ ±1 tiếng
    - user_id lấy từ JWT token
    """
    try:
        return await crud_booking.create_booking(
            db=db, obj_in=booking_in, user_id=current_user.id
        )
    except (RestaurantNotFound, CapacityExceeded, TimeSlotConflict) as exc:
        _handle_booking_domain_error(exc)


@router.patch("/{booking_id}", response_model=BookingRead)
async def update_existing_booking(
    booking_id: int,
    booking_in: BookingUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Cập nhật thông tin hoặc hủy booking (status='cancelled').
    Chỉ chủ nhân booking mới có quyền.
    Tự động kiểm tra lại sức chứa nếu ngày/giờ/số khách thay đổi.
    """
    try:
        return await crud_booking.update_booking(
            db=db,
            booking_id=booking_id,
            obj_in=booking_in,
            user_id=current_user.id,
        )
    except (BookingNotFound, CapacityExceeded, TimeSlotConflict) as exc:
        _handle_booking_domain_error(exc)


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_booking(
    booking_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Xóa vĩnh viễn đơn đặt bàn. Chỉ chủ sở hữu mới có quyền xóa.
    """
    try:
        await crud_booking.delete_booking(
            db=db, booking_id=booking_id, user_id=current_user.id
        )
    except BookingNotFound as exc:
        _handle_booking_domain_error(exc)
    return None