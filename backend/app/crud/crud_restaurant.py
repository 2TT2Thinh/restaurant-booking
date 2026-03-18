from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate

# Lấy danh sách nhà hàng (có tìm kiếm)
async def get_all_restaurants(
    db: AsyncSession,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Restaurant]:
    query = select(Restaurant)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.where(Restaurant.name.ilike(search_term))

    query = query.order_by(Restaurant.name).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Lấy 1 nhà hàng theo ID
async def get_restaurant_by_id(db: AsyncSession, restaurant_id: int):
    return await db.get(Restaurant, restaurant_id)

# Admin: Tạo nhà hàng mới
async def create_restaurant(db: AsyncSession, obj_in: RestaurantCreate) -> Restaurant:
    new_restaurant = Restaurant(**obj_in.model_dump())
    db.add(new_restaurant)
    await db.commit()
    await db.refresh(new_restaurant)
    return new_restaurant

# Admin: Sửa nhà hàng
async def update_restaurant(
    db: AsyncSession,
    restaurant_id: int,
    obj_in: RestaurantUpdate
) -> Optional[Restaurant]:
    db_obj = await db.get(Restaurant, restaurant_id)
    if not db_obj:
        return None

    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

# Admin: Xóa nhà hàng
async def delete_restaurant(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
    db_obj = await db.get(Restaurant, restaurant_id)
    if not db_obj:
        return None

    await db.delete(db_obj)
    await db.commit()
    return db_obj