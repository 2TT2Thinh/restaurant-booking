from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, create_access_token
from fastapi import HTTPException, status
from app.schemas.auth import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security import getpassword_hash
# check login (nếu email, password và tài khoán còn hoạt động không đúng thì trả về user, ngược lại trả về None)
async def authenticate_user(db: Session, email: str, password: str):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User inactive")
    return user

# resister user
async def create_user(db: AsyncSession, user_data: UserCreate):
    # 1. Kiểm tra xem email đã tồn tại chưa
    check_query = await db.execute(select(User).filter(User.email == user_data.email))
    
    if check_query.scalars().first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # 2. Tạo đối tượng User mới từ thông tin bảng bạn đưa
    new_user = User(
        email=user_data.email,
        hashed_password=getpassword_hash(user_data.password),
        full_name=user_data.full_name,
        phone=user_data.phone
    )
    
    db.add(new_user)
    try:
        await db.commit() # Lưu vào DB
        await db.refresh(new_user) # Lấy lại dữ liệu sau khi lưu (để có id và created_at)
        return new_user
    except Exception as e:
        await db.rollback() # Nếu có lỗi, rollback lại
        raise HTTPException(status_code=500, detail="Internal Server Error")