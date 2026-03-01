from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud import crud_booking
from app.schemas.booking import BookingRead
from app.models.user import User
from app.schemas.booking import BookingCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import api_key_scheme
router = APIRouter()

@router.get("/me", response_model=List[BookingRead])
async def read_my_bookings(
    token: str = Depends(api_key_scheme), # Swagger sẽ hiện ô Value cho cái này
    db: AsyncSession = Depends(deps.get_db), # Đảm bảo deps trả về AsyncSession
    current_user: User = Depends(deps.get_current_user)
):
    # Gọi hàm crud và phải có await vì nó là async def
    bookings = await crud_booking.get_user_bookings(db, user_id=current_user.id)
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