# app/models/restaurant.py
from sqlalchemy import Column, Integer, String, Text, Time, DateTime, CheckConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(255), nullable=False, index=True)
    address       = Column(Text, nullable=False)
    phone         = Column(String(20))
    cuisine_type  = Column(String(100), index=True)
    opening_time  = Column(Time)
    closing_time  = Column(Time)
    max_capacity  = Column(Integer, nullable=False, default=50, server_default="50")
    created_at    = Column(DateTime, server_default=func.now())
    updated_at    = Column(DateTime, server_default=func.now(), onupdate=func.now())

    bookings = relationship("Booking", back_populates="restaurant")

    __table_args__ = (
        CheckConstraint("max_capacity > 0",                    name="check_capacity"),
        CheckConstraint("opening_time < closing_time OR opening_time IS NULL",
                        name="check_opening_before_closing"),
        Index("ix_restaurants_cuisine", "cuisine_type"),
    )