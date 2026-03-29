# app/services/auth_service.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.auth import UserCreate
from app.core.security import verify_password, get_password_hash


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> User | None:
    """
    Returns User if credentials are valid and account is active.
    Returns None if email not found or password is wrong.
    Raises HTTPException(400) if account is deactivated.
    """
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        # Distinguish deactivated account from wrong credentials
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản đã bị vô hiệu hóa. Vui lòng liên hệ quản trị viên.",
        )
    return user


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Creates a new user. Raises HTTPException(400) if email already exists.
    """
    existing = await db.execute(select(User).where(User.email == user_data.email))
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã được sử dụng",
        )

    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        phone=user_data.phone,
    )

    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        await db.rollback()
        # Log the actual error server-side, return generic message to client
        print(f"[create_user] Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi hệ thống. Vui lòng thử lại sau.",
        )