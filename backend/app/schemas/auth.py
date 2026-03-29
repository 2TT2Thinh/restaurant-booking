from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

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
    phone: Optional[str] = None          # SỬA: Optional cho đúng thực tế
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Mật khẩu phải có ít nhất 8 ký tự')
        if not any(c.isupper() for c in v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ hoa')
        if not any(c.isdigit() for c in v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ số')
        return v

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone: Optional[str] = None          # SỬA: Optional vì không bắt buộc
    role: str                             # THÊM
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True