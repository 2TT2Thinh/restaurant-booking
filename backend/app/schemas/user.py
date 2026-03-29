# app/schemas/user.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from app.schemas.auth import _validate_password


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None

    @field_validator("full_name")
    @classmethod
    def full_name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Họ tên không được để trống")
        return v.strip() if v else v


class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        return _validate_password(v)

    @field_validator("new_password")
    @classmethod
    def passwords_must_differ(cls, v: str, info) -> str:
        # Prevent setting new password identical to current (caught at schema level)
        # Full check (against hash) still happens in the endpoint
        if info.data.get("current_password") == v:
            raise ValueError("Mật khẩu mới phải khác mật khẩu hiện tại")
        return v


class UserRead(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}