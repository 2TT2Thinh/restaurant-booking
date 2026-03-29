from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import LoginSchema, TokenSchema
from app.services.auth_service import authenticate_user, create_user
from app.core.security import create_access_token
from app.api.deps import get_db
from app.schemas.auth import UserCreate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()
@router.post("/login", response_model=TokenSchema)
async def login(
    data: LoginSchema,
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # create_user ném HTTPException(400) nếu email tồn tại — để nó truyền lên
    user = await create_user(db, user_in)
    return user
# @router.post("/create-admin-temp")
# async def create_admin_temp(
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Endpoint tạm để tạo admin - XÓA SAU KHI DÙNG
#     """
#     from app.services.auth_service import create_user
#     from app.schemas.auth import UserCreate
    
#     user_in = UserCreate(
#         email="admin@bookingtracker.com",
#         password="Admin@123456",
#         full_name="Super Admin",
#         phone="0909000000"
#     )
    
#     user = await create_user(db, user_in)
#     if not user:
#         raise HTTPException(status_code=400, detail="Email đã tồn tại")
    
#     # Set role admin
#     user.role = "admin"
#     db.add(user)
#     await db.commit()
#     await db.refresh(user)
    
#     return {
#         "message": "Admin created!",
#         "email": user.email,
#         "role": user.role
#     }
