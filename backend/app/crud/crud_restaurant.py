# app/crud/crud_restaurant.py
from typing import List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


async def get_all_restaurants(
    db: AsyncSession,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
) -> Tuple[List[Restaurant], int]:
    """Returns (items, total) for paginated response envelope."""
    filters = []
    if search:
        filters.append(Restaurant.name.ilike(f"%{search.strip()}%"))

    count_q = select(func.count(Restaurant.id)).where(*filters)
    data_q  = (
        select(Restaurant)
        .where(*filters)
        .order_by(Restaurant.name)
        .offset(skip)
        .limit(limit)
    )

    total  = await db.scalar(count_q) or 0
    result = await db.execute(data_q)
    return result.scalars().all(), total


async def get_restaurant_by_id(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
    return await db.get(Restaurant, restaurant_id)


async def create_restaurant(db: AsyncSession, obj_in: RestaurantCreate) -> Restaurant:
    new_restaurant = Restaurant(**obj_in.model_dump())
    db.add(new_restaurant)
    await db.commit()
    await db.refresh(new_restaurant)
    return new_restaurant


async def update_restaurant(
    db: AsyncSession, restaurant_id: int, obj_in: RestaurantUpdate
) -> Optional[Restaurant]:
    db_obj = await db.get(Restaurant, restaurant_id)
    if not db_obj:
        return None
    for field, value in obj_in.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_restaurant(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
    db_obj = await db.get(Restaurant, restaurant_id)
    if not db_obj:
        return None
    await db.delete(db_obj)
    await db.commit()
    return db_obj