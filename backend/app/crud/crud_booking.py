# app/crud/crud_booking.py
from typing import List, Optional
from datetime import datetime, timezone, timedelta, time as time_type

from sqlalchemy import func, or_, select, and_, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, contains_eager

from app.models.booking import Booking
from app.models.restaurant import Restaurant
from app.schemas.booking import BookingCreate, BookingUpdate
from app.exceptions import (
    RestaurantNotFound,
    CapacityExceeded,
    TimeSlotConflict,
    BookingNotFound,
)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _time_window(booking_time: time_type, window_hours: int = 2):
    """
    Returns (start_time, end_time) representing the overlap window around a booking.
    A 2-hour window means: any booking within ±1 hour competes for capacity.
    Clamps to 00:00 and 23:59 so no overflow across midnight.
    """
    base = datetime.combine(datetime.today(), booking_time)
    start = (base - timedelta(hours=window_hours // 2)).time()
    end   = (base + timedelta(hours=window_hours // 2)).time()
    # Clamp to valid time range
    start = max(start, time_type(0, 0))
    end   = min(end,   time_type(23, 59, 59))
    return start, end


async def _get_booked_guests_in_window(
    db: AsyncSession,
    restaurant_id: int,
    booking_date,
    booking_time: time_type,
    exclude_booking_id: Optional[int] = None,
) -> int:
    """
    Sum number_of_guests for all non-cancelled bookings at this restaurant
    whose booking_time falls within the ±1h window around booking_time.
    Optionally exclude a booking ID (used during updates).
    """
    start, end = _time_window(booking_time)

    conditions = [
        Booking.restaurant_id == restaurant_id,
        Booking.booking_date == booking_date,
        Booking.booking_time >= start,
        Booking.booking_time <= end,
        Booking.status != "cancelled",
    ]
    if exclude_booking_id is not None:
        conditions.append(Booking.id != exclude_booking_id)

    total = await db.scalar(
        select(func.coalesce(func.sum(Booking.number_of_guests), 0)).where(
            and_(*conditions)
        )
    )
    return int(total)


# ---------------------------------------------------------------------------
# Public CRUD functions
# ---------------------------------------------------------------------------

async def get_user_bookings(db: AsyncSession, user_id: int) -> List[Booking]:
    query = (
        select(Booking)
        .options(selectinload(Booking.restaurant))
        .where(Booking.user_id == user_id)
        .order_by(Booking.created_at.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()


async def create_booking(
    db: AsyncSession, obj_in: BookingCreate, user_id: int
) -> Booking:
    # 1. Restaurant must exist
    restaurant = await db.get(Restaurant, obj_in.restaurant_id)
    if not restaurant:
        raise RestaurantNotFound()

    # 2. Capacity check: sum existing guests in ±1h window + new guests vs max_capacity
    booked = await _get_booked_guests_in_window(
        db,
        restaurant_id=obj_in.restaurant_id,
        booking_date=obj_in.booking_date,
        booking_time=obj_in.booking_time,
    )
    available = restaurant.max_capacity - booked
    if obj_in.number_of_guests > available:
        if available <= 0:
            raise TimeSlotConflict()
        raise CapacityExceeded(max_capacity=restaurant.max_capacity, available=available)

    # 3. Create booking
    new_booking = Booking(
        **obj_in.model_dump(),
        user_id=user_id,
        status="pending",
    )
    db.add(new_booking)
    await db.commit()

    # 4. Re-fetch with relationship loaded (new_booking is expired after commit)
    result = await db.execute(
        select(Booking)
        .options(selectinload(Booking.restaurant))
        .where(Booking.id == new_booking.id)
    )
    return result.scalars().first()


async def update_booking(
    db: AsyncSession,
    booking_id: int,
    obj_in: BookingUpdate,
    user_id: int,
) -> Booking:
    # 1. Fetch with relationship pre-loaded
    result = await db.execute(
        select(Booking)
        .options(selectinload(Booking.restaurant))
        .where(Booking.id == booking_id, Booking.user_id == user_id)
    )
    db_obj = result.scalars().first()

    if not db_obj:
        raise BookingNotFound()

    update_data = obj_in.model_dump(exclude_unset=True)

    # 2. If date/time/guests are changing, re-check capacity
    new_date   = update_data.get("booking_date",   db_obj.booking_date)
    new_time   = update_data.get("booking_time",   db_obj.booking_time)
    new_guests = update_data.get("number_of_guests", db_obj.number_of_guests)
    new_status = update_data.get("status", db_obj.status)

    date_time_guests_changed = any(
        k in update_data for k in ("booking_date", "booking_time", "number_of_guests")
    )

    if date_time_guests_changed and new_status != "cancelled":
        restaurant = db_obj.restaurant  # already loaded via selectinload
        booked = await _get_booked_guests_in_window(
            db,
            restaurant_id=db_obj.restaurant_id,
            booking_date=new_date,
            booking_time=new_time,
            exclude_booking_id=booking_id,  # exclude self when rechecking
        )
        available = restaurant.max_capacity - booked
        if new_guests > available:
            if available <= 0:
                raise TimeSlotConflict()
            raise CapacityExceeded(max_capacity=restaurant.max_capacity, available=available)

    # 3. Apply updates
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.commit()

    # 4. Re-fetch to return fresh state
    result = await db.execute(
        select(Booking)
        .options(selectinload(Booking.restaurant))
        .where(Booking.id == db_obj.id)
    )
    return result.scalars().first()


async def delete_booking(
    db: AsyncSession, booking_id: int, user_id: int
) -> Booking:
    result = await db.execute(
        select(Booking).where(
            Booking.id == booking_id, Booking.user_id == user_id
        )
    )
    db_obj = result.scalars().first()

    if not db_obj:
        raise BookingNotFound()

    await db.delete(db_obj)
    await db.commit()
    return db_obj


async def get_multi_bookings(
    db: AsyncSession,
    user_id: int,
    search: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
) -> List[Booking]:
    if search:
        # JOIN + contains_eager: single query for both filter and relationship load
        query = (
            select(Booking)
            .join(Restaurant, Booking.restaurant_id == Restaurant.id)
            .options(contains_eager(Booking.restaurant))
            .where(
                Booking.user_id == user_id,
                Restaurant.name.ilike(f"%{search.strip()}%"),
            )
        )
    else:
        query = (
            select(Booking)
            .options(selectinload(Booking.restaurant))
            .where(Booking.user_id == user_id)
        )

    if status and status.lower() != "all":
        query = query.where(Booking.status == status.lower())

    query = query.order_by(Booking.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_booking_stats(db: AsyncSession, user_id: int) -> dict:
    now_utc      = datetime.now(timezone.utc).replace(tzinfo=None)
    current_date = now_utc.date()
    current_time = now_utc.time()

    query = select(
        func.count(Booking.id).label("total"),
        func.count(case((Booking.status == "confirmed", 1))).label("confirmed"),
        func.count(case((Booking.status == "cancelled", 1))).label("cancelled"),
        func.count(case((
            and_(
                Booking.status == "pending",
                or_(
                    Booking.booking_date > current_date,
                    and_(
                        Booking.booking_date == current_date,
                        Booking.booking_time >= current_time,
                    ),
                ),
            ),
            1,
        ))).label("pending"),
        func.count(case((
            and_(
                Booking.status == "pending",
                or_(
                    Booking.booking_date < current_date,
                    and_(
                        Booking.booking_date == current_date,
                        Booking.booking_time < current_time,
                    ),
                ),
            ),
            1,
        ))).label("expired"),
    ).where(Booking.user_id == user_id)

    row = (await db.execute(query)).one()
    return {
        "total":     row.total     or 0,
        "confirmed": row.confirmed or 0,
        "cancelled": row.cancelled or 0,
        "pending":   row.pending   or 0,
        "expired":   row.expired   or 0,
    }