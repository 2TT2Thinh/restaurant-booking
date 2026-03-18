from pydantic import BaseModel
from datetime import time, datetime
from typing import Optional

class RestaurantBase(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None
    cuisine_type: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    max_capacity: int = 50

class RestaurantCreate(RestaurantBase):  # Admin dùng để tạo
    pass

class RestaurantUpdate(BaseModel):       # Admin dùng để sửa
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    cuisine_type: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    max_capacity: Optional[int] = None

class RestaurantRead(RestaurantBase):    # Trả về cho frontend
    id: int
    created_at: datetime

    class Config:
        from_attributes = True