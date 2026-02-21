# SỬA DÒNG NÀY:
from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Text, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from app.models.base import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    restaurant_name = Column(String(255), nullable=False)
    restaurant_address = Column(Text)
   # TRONG CLASS BOOKING:
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    booking_date = Column(Date, nullable=False)
    booking_time = Column(Time, nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    status = Column(String(20), server_default="pending")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Ràng buộc số khách > 0
    __table_args__ = (
        CheckConstraint('number_of_guests > 0', name='check_guests'),
    )