from pydantic import BaseModel, Field, computed_field
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
    @computed_field
    @property
    def full_datetime(self) -> datetime:
        # Tự động gộp ngày và giờ từ chính object này
        return datetime.combine(self.booking_date, self.booking_time)
    class Config:
        from_attributes = True # Cho phép chuyển từ SQLAlchemy model sang Pydantic


class BookingCreate(BaseModel):
    restaurant_name: str = Field(..., example="Nhà hàng Hải Sản Biển Đông")
    restaurant_address: Optional[str] = None
    booking_date: date
    booking_time: datetime
    number_of_guests: int = Field(..., gt=0) # Phải lớn hơn 0
    latitude: Optional[float] = None
    longitude: Optional[float] = None



class BookingUpdate(BaseModel):
    restaurant_name: Optional[str] = None
    restaurant_address: Optional[str] = None
    booking_date: Optional[date] = None
    booking_time: Optional[time] = None
    number_of_guests: Optional[int] = None
    status: Optional[str] = None # Dùng để đổi sang "cancelled"




