from sqlalchemy import Column, Integer, String, Text, Time, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    address = Column(Text, nullable=False)
    phone = Column(String(20))
    cuisine_type = Column(String(100))        # Ví dụ: "Việt Nam", "Nhật", "Hàn"
    opening_time = Column(Time)               # Giờ mở cửa
    closing_time = Column(Time)               # Giờ đóng cửa
    max_capacity = Column(Integer, default=50) # Số khách tối đa
    created_at = Column(DateTime, server_default=func.now())

    # Relationship: 1 nhà hàng có nhiều booking
    bookings = relationship("Booking", back_populates="restaurant")

    __table_args__ = (
        CheckConstraint('max_capacity > 0', name='check_capacity'),
    )