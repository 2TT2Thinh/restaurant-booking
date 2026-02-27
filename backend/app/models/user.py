from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy import Boolean
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)