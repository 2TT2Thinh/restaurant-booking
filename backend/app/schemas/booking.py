from pydantic import BaseModel, Field, computed_field
from datetime import date, time, datetime
from typing import Optional

# Schema nhà hàng lồng trong booking (để trả về cho frontend)
class RestaurantInBooking(BaseModel):
    id: int
    name: str
    address: str
    cuisine_type: Optional[str] = None

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    booking_date: date
    booking_time: time                    # SỬA: đổi từ datetime → time cho đúng
    number_of_guests: int
    special_notes: Optional[str] = None  # THÊM: thay latitude/longitude

class BookingCreate(BookingBase):
    restaurant_id: int                    # THAY: bỏ restaurant_name, nhận ID

class BookingUpdate(BaseModel):
    booking_date: Optional[date] = None
    booking_time: Optional[time] = None
    number_of_guests: Optional[int] = Field(default=None, gt=0)
    special_notes: Optional[str] = None
    status: Optional[str] = None         # Dùng để đổi sang "cancelled"

class BookingRead(BookingBase):
    id: int
    status: str
    created_at: datetime
    restaurant_id: int   
    restaurant: RestaurantInBooking       # THÊM: trả về info nhà hàng thay vì tên string

    @computed_field
    @property
    def full_datetime(self) -> datetime:
        return datetime.combine(self.booking_date, self.booking_time)

    class Config:
        from_attributes = True