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
api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)
# 2. Hàm lấy DB cục bộ (để dùng ngay trong file này)
async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session

# 3. Hàm lấy User hiện tại
async def get_current_user(
    api_key: Optional[str] = Depends(api_key_scheme),
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    
    # Định nghĩa lỗi tập trung
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 1. Xác định Token thực tế (Ưu tiên lấy từ api_key nếu có Bearer)
    actual_token = token
    if api_key and api_key.startswith("Bearer "):
        actual_token = api_key.split(" ")[1]

    try:
        # 2. Giải mã JWT
        payload = jwt.decode(
            actual_token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        # Vì hàm login của bạn dùng subject=user.email, nên sub ở đây là email
        user_email: str = payload.get("sub")
        if not user_email:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # 3. Truy vấn User theo Email (Bỏ int() vì user_email là chuỗi)
    # Tìm chính xác theo cột email trong Database
    result = await db.execute(select(User).where(User.email == user_email))
    user = result.scalars().first()

    # 4. Kiểm tra User tồn tại và trạng thái
    if not user:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User account is inactive"
        )
        
    return user