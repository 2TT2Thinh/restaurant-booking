from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr

# Schema cơ bản (Dùng chung)
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = True

# update user
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
# 4. Dùng để trả về dữ liệu (Read) - Không bao giờ trả về password!
class UserRead(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True