from typing import AsyncGenerator
from app.db.session import AsyncSessionLocal # Đảm bảo đúng tên này
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models.user import User
from sqlalchemy import select

# 1. Khai báo token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")
# 2. Hàm lấy DB cục bộ (để dùng ngay trong file này)
async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session


# 3. Hàm lấy User hiện tại
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db) # Dùng hàm get_db vừa định nghĩa ở trên
) -> User:
    
    # Định nghĩa lỗi tập trung để tái sử dụng
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Giải mã JWT
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # Truy vấn User theo phong cách SQLAlchemy 2.0 Async
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()

    if not user or not user.is_active: # Kiểm tra thêm cả trạng thái active
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found or inactive"
        )
        
    return user