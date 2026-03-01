from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional

class BookingBase(BaseModel):
    restaurant_name: str
    restaurant_address: Optional[str] = None
    booking_date: date
    booking_time: time
    number_of_guests: int
    status: str = "pending"

class BookingRead(BookingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # Cho phép chuyển từ SQLAlchemy model sang Pydantic





class BookingCreate(BaseModel):
    restaurant_name: str = Field(..., example="Nhà hàng Hải Sản Biển Đông")
    restaurant_address: Optional[str] = None
    booking_date: date
    booking_time: time
    number_of_guests: int = Field(..., gt=0) # Phải lớn hơn 0
    latitude: Optional[float] = None
    longitude: Optional[float] = None