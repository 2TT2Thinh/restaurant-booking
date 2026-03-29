from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Text, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy import Enum as SAEnum
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="RESTRICT")) 

    booking_date = Column(Date, nullable=False)
    booking_time = Column(Time, nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    special_notes = Column(Text)                        # GHI CHÚ thêm, thay latitude/longitude
    status = Column(
    SAEnum("pending", "confirmed", "cancelled", name="booking_status"),
    nullable=False,
    server_default="pending"
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship ngược lại
    user = relationship("User", back_populates="bookings")
    restaurant = relationship("Restaurant", back_populates="bookings")

    __table_args__ = (
        CheckConstraint('number_of_guests > 0', name='check_guests'),
    )