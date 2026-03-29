from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    @field_validator('new_password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Mật khẩu phải có ít nhất 8 ký tự')
        return v

class UserRead(UserBase):
    id: int
    role: str                             # THÊM: để frontend biết là admin hay customer
    created_at: datetime

    class Config:
        from_attributes = True