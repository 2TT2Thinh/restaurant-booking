from typing import AsyncGenerator
from app.db.session import AsyncSessionLocal # Đảm bảo đúng tên này
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models.user import User
from sqlalchemy import select
from fastapi.security import APIKeyHeader
from typing import Optional
# 1. Khai báo token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")
# Khai báo thêm một kiểu bảo mật nữa để dán Token thủ công

# 2. Hàm lấy DB cục bộ (để dùng ngay trong file này)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

# 3. Hàm lấy User hiện tại
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin đăng nhập",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")
        if not user_email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.email == user_email))
    user = result.scalars().first()
    if not user:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tài khoản đã bị vô hiệu hóa")
    return user

# Thêm vào cuối file deps.py
async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Chỉ cho phép user có role = 'admin' truy cập"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền thực hiện hành động này"
        )
    return current_user