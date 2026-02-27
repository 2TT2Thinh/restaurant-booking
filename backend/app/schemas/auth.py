from pydantic import BaseModel, EmailStr
from datetime import datetime
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


# resgister schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: str | None = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone: str
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True