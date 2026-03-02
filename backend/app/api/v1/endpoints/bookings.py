from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.crud import crud_booking
from app.schemas.booking import BookingRead
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import api_key_scheme

router = APIRouter()

@router.get("/me", response_model=List[BookingRead])
async def read_my_bookings(
   # Các tham số lọc (Query Parameters) - Mặc định là None (Lấy tất cả)
    search: Optional[str] = None, 
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db), # Đảm bảo deps trả về AsyncSession
    current_user: User = Depends(deps.get_current_user)
):
    # Gọi hàm crud và phải có await vì nó là async def
    bookings = await crud_booking.get_multi_bookings(
        db=db, 
        user_id=current_user.id, 
        search=search, 
        status=status,
        skip=skip, 
        limit=limit
    )
    return bookings


@router.post("/", response_model=BookingRead, status_code= status.HTTP_201_CREATED)
async def create_new_booking(
    booking_in: BookingCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user) # Bảo mật: Chỉ ai login mới đặt được
):
    """
    Tạo một đơn đặt bàn mới.
    user_id được lấy tự động từ Token.
    """
    return await crud_booking.create_booking(
        db=db, 
        obj_in=booking_in, 
        user_id=current_user.id
    )


@router.patch("/{booking_id}", response_model=BookingRead)
async def update_existing_booking(
    booking_id: int,
    booking_in: BookingUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    Cập nhật thông tin đặt bàn hoặc Hủy (đổi status sang 'cancelled').
    Chỉ chủ nhân của đơn đặt bàn mới có quyền thực hiện.
    """
    updated_booking = await crud_booking.update_booking(
        db=db, 
        booking_id=booking_id, 
        obj_in=booking_in, 
        user_id=current_user.id
    )
    
    if not updated_booking:
        raise HTTPException(
            status_code=404, 
            detail="Không tìm thấy đơn đặt bàn hoặc bạn không có quyền chỉnh sửa"
        )
        
    return updated_booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_booking(
    booking_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    Xóa vĩnh viễn một đơn đặt bàn.
    Chỉ chủ sở hữu mới có quyền xóa. 
    Trả về 204 No Content nếu thành công.
    """
    deleted_booking = await crud_booking.delete_booking(
        db=db, 
        booking_id=booking_id, 
        user_id=current_user.id
    )
    
    if not deleted_booking:
        raise HTTPException(
            status_code=404, 
            detail="Không tìm thấy đơn đặt bàn để xóa hoặc bạn không có quyền"
        )
    
    # Với DELETE thành công, thường trả về null và code 204
    return None

