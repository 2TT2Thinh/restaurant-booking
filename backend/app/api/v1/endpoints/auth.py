# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import TokenSchema, UserCreate, UserResponse
from app.services.auth_service import authenticate_user, create_user
from app.core.security import create_access_token
from app.api.deps import get_db

router = APIRouter()


@router.post("/login", response_model=TokenSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    OAuth2-compatible login endpoint.
    - Accepts: application/x-www-form-urlencoded (username + password)
    - 'username' field is treated as email
    - Returns: Bearer JWT token
    - Works with Swagger UI Authorize button
    """
    user = await authenticate_user(db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Đăng ký tài khoản mới.
    Accepts: application/json
    create_user raises HTTPException(400) if email already exists.
    """
    return await create_user(db, user_in)