# app/models/booking.py
import enum
from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Text, ForeignKey, CheckConstraint, Enum as SAEnum, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class BookingStatus(str, enum.Enum):
    pending   = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    restaurant_id   = Column(Integer, ForeignKey("restaurants.id", ondelete="RESTRICT"), nullable=False)

    booking_date    = Column(Date,    nullable=False)
    booking_time    = Column(Time,    nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    special_notes   = Column(Text)
    status          = Column(
        SAEnum(BookingStatus, name="booking_status"),
        nullable=False,
        server_default=BookingStatus.pending.value,
    )
    created_at      = Column(DateTime, server_default=func.now())
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user       = relationship("User",       back_populates="bookings")
    restaurant = relationship("Restaurant", back_populates="bookings")

    __table_args__ = (
        CheckConstraint("number_of_guests > 0", name="check_guests"),
        # Composite index for the capacity-check query (most frequent)
        Index("ix_bookings_restaurant_date", "restaurant_id", "booking_date"),
        Index("ix_bookings_user_created",    "user_id",       "created_at"),
        Index("ix_bookings_status",          "status"),
    )