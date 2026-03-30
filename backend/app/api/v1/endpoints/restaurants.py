# app/api/v1/endpoints/restaurants.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.api import deps
from app.crud import crud_restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantRead
from app.schemas.response import PagedResponse, DataResponse
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=PagedResponse[RestaurantRead])
async def list_restaurants(
    search: Optional[str] = None,
    skip: int  = Query(default=0,  ge=0),
    limit: int = Query(default=20, le=100),
    db: AsyncSession = Depends(deps.get_db),
):
    items, total = await crud_restaurant.get_all_restaurants(
        db, search=search, skip=skip, limit=limit
    )
    return PagedResponse.create(items=items, total=total, skip=skip, limit=limit)


@router.get("/{restaurant_id}", response_model=DataResponse[RestaurantRead])
async def get_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(deps.get_db),
):
    restaurant = await crud_restaurant.get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà hàng")
    return DataResponse.create(restaurant)


@router.post("/", response_model=DataResponse[RestaurantRead], status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    obj_in: RestaurantCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin),
):
    restaurant = await crud_restaurant.create_restaurant(db, obj_in)
    return DataResponse.create(restaurant)


@router.patch("/{restaurant_id}", response_model=DataResponse[RestaurantRead])
async def update_restaurant(
    restaurant_id: int,
    obj_in: RestaurantUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin),
):
    updated = await crud_restaurant.update_restaurant(db, restaurant_id, obj_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà hàng")
    return DataResponse.create(updated)


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin),
):
    deleted = await crud_restaurant.delete_restaurant(db, restaurant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà hàng")
    return None