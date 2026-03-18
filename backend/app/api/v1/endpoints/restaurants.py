from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.api import deps
from app.crud import crud_restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantRead
from app.models.user import User

router = APIRouter()

# Tất cả mọi người đều xem được danh sách nhà hàng
@router.get("/", response_model=List[RestaurantRead])
async def list_restaurants(
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db)
):
    return await crud_restaurant.get_all_restaurants(db, search=search, skip=skip, limit=limit)

# Xem chi tiết 1 nhà hàng
@router.get("/{restaurant_id}", response_model=RestaurantRead)
async def get_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    restaurant = await crud_restaurant.get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà hàng")
    return restaurant

# ===== ADMIN ONLY =====
@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    obj_in: RestaurantCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)  # Chỉ admin
):
    return await crud_restaurant.create_restaurant(db, obj_in)

@router.patch("/{restaurant_id}", response_model=RestaurantRead)
async def update_restaurant(
    restaurant_id: int,
    obj_in: RestaurantUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)  # Chỉ admin
):
    updated = await crud_restaurant.update_restaurant(db, restaurant_id, obj_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà hàng")
    return updated

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)  # Chỉ admin
):
    deleted = await crud_restaurant.delete_restaurant(db, restaurant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà hàng")
    return None