# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
import re


def _validate_password(v: str) -> str:
    """
    Shared password strength rules.
    Used by both UserCreate (register) and PasswordChange (change-password).
    """
    if len(v) < 8:
        raise ValueError("Mật khẩu phải có ít nhất 8 ký tự")
    if not any(c.isupper() for c in v):
        raise ValueError("Mật khẩu phải có ít nhất 1 chữ hoa")
    if not any(c.islower() for c in v):
        raise ValueError("Mật khẩu phải có ít nhất 1 chữ thường")
    if not any(c.isdigit() for c in v):
        raise ValueError("Mật khẩu phải có ít nhất 1 chữ số")
    return v


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        return _validate_password(v)

    @field_validator("full_name")
    @classmethod
    def full_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Họ tên không được để trống")
        return v.strip()


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    role: str
    created_at: datetime
    is_active: bool = True

    model_config = {"from_attributes": True}