from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.user import PasswordChange, UserRead, UserUpdate
from app.crud import crud_booking  # Import để dùng hàm stats
from app.models.user import User
from app.core.security import getpassword_hash, verify_password

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def read_user_me(
    current_user: User = Depends(deps.get_current_user)
):
    """Lấy thông tin profile của chính tôi"""
    return current_user

@router.get("/me/stats")
async def read_my_stats(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Lấy các con số thống kê (48, 42, 6) cho trang Profile"""
    # Hàm này mình đã viết ở crud_booking trước đó
    return await crud_booking.get_booking_stats(db, user_id=current_user.id)

@router.patch("/me", response_model=UserRead)
async def update_user_profile(
    obj_in: UserUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Cập nhật Họ tên và Số điện thoại từ form Profile"""
    update_data = obj_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user
@router.post("/me/change-password")
async def change_my_password(
    obj_in: PasswordChange,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Đổi mật khẩu cho người dùng hiện tại.
    Yêu cầu: Nhập đúng mật khẩu cũ mới cho phép đổi mật khẩu mới.
    """
    # 1. Kiểm tra mật khẩu cũ (verify hash)
    if not verify_password(obj_in.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Mật khẩu hiện tại không chính xác"
        )
    
    # 2. Băm mật khẩu mới và cập nhật vào model
    current_user.hashed_password = getpassword_hash(obj_in.new_password)
    
    # 3. Lưu vào database
    db.add(current_user)
    await db.commit()
    
    return {"message": "Đổi mật khẩu thành công! Vui lòng sử dụng mật khẩu mới cho lần đăng nhập sau."}