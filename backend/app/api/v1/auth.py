from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import LoginSchema, TokenSchema
from app.services.auth_service import authenticate_user
from app.core.security import create_access_token
from app.api.deps import get_db

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