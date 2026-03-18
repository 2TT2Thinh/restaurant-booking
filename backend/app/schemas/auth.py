from pydantic import BaseModel, EmailStr
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