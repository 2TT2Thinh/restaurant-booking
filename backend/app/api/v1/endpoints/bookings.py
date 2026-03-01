from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud import crud_booking
from app.schemas.booking import BookingRead
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=List[BookingRead])
async def read_my_bookings(
    db: Session = Depends(deps.get_db), # Đảm bảo deps trả về AsyncSession
    current_user: User = Depends(deps.get_current_user)
):
    # Gọi hàm crud và phải có await vì nó là async def
    bookings = await crud_booking.get_user_bookings(db, user_id=current_user.id)
    return bookings