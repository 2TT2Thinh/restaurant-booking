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
    db: Session = Depends(get_db),
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

@router.post("/register", response_model= UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, user_in)
    if not user:
     raise HTTPException(    
        status_code= 400,
        detail="Email đã tồn tại"
        )
    return  user
    