# app/services/smart_booking_service.py
"""
Smart Booking Suggestions.
All logic is SQL aggregation over the existing bookings table.
No external dependencies.

Provides:
  1. analyze_slot()       — is this slot peak? how full?
  2. suggest_time_slots() — alternative times on same day
  3. suggest_dates()      — alternative dates for same time
"""
from datetime import date, time, datetime, timedelta
from typing import Optional
from dataclasses import dataclass

from sqlalchemy import func, select, and_, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, BookingStatus
from app.models.restaurant import Restaurant


PEAK_THRESHOLD = 0.70   # >70% capacity = peak
WINDOW_HOURS   = 1      # ±1h window for capacity check (matches crud_booking)


@dataclass
class SlotAnalysis:
    restaurant_id:   int
    booking_date:    date
    booking_time:    time
    max_capacity:    int
    booked_guests:   int
    available:       int
    occupancy_rate:  float   # 0.0–1.0
    is_peak:         bool
    label:           str     # "Bình thường" | "Đông" | "Rất đông" | "Đầy"


@dataclass
class SlotSuggestion:
    booking_time:   time
    available:      int
    occupancy_rate: float
    label:          str


@dataclass
class DateSuggestion:
    booking_date:   date
    booking_time:   time
    available:      int
    occupancy_rate: float


def _occupancy_label(rate: float) -> str:
    if rate >= 1.0:  return "Đầy chỗ"
    if rate >= 0.70: return "Rất đông"
    if rate >= 0.40: return "Đông vừa"
    return "Còn nhiều chỗ"


async def _booked_in_window(
    db: AsyncSession,
    restaurant_id: int,
    booking_date: date,
    booking_time: time,
    exclude_booking_id: Optional[int] = None,
) -> int:
    """Sum guests in ±WINDOW_HOURS around booking_time."""
    base  = datetime.combine(booking_date, booking_time)
    start = (base - timedelta(hours=WINDOW_HOURS)).time()
    end   = (base + timedelta(hours=WINDOW_HOURS)).time()

    conditions = [
        Booking.restaurant_id == restaurant_id,
        Booking.booking_date  == booking_date,
        Booking.booking_time  >= start,
        Booking.booking_time  <= end,
        Booking.status        != BookingStatus.cancelled,
    ]
    if exclude_booking_id:
        conditions.append(Booking.id != exclude_booking_id)

    total = await db.scalar(
        select(func.coalesce(func.sum(Booking.number_of_guests), 0))
        .where(and_(*conditions))
    )
    return int(total)


async def analyze_slot(
    db: AsyncSession,
    restaurant_id: int,
    booking_date: date,
    booking_time: time,
    guests: int = 1,
) -> SlotAnalysis:
    """
    Analyzes a specific (restaurant, date, time) slot.
    Returns occupancy info and whether it's peak.
    """
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise ValueError(f"Restaurant {restaurant_id} not found")

    booked    = await _booked_in_window(db, restaurant_id, booking_date, booking_time)
    available = max(restaurant.max_capacity - booked, 0)
    rate      = booked / restaurant.max_capacity if restaurant.max_capacity else 0.0

    return SlotAnalysis(
        restaurant_id  = restaurant_id,
        booking_date   = booking_date,
        booking_time   = booking_time,
        max_capacity   = restaurant.max_capacity,
        booked_guests  = booked,
        available      = available,
        occupancy_rate = round(rate, 3),
        is_peak        = rate >= PEAK_THRESHOLD,
        label          = _occupancy_label(rate),
    )


async def suggest_time_slots(
    db: AsyncSession,
    restaurant_id: int,
    booking_date: date,
    preferred_time: time,
    guests: int,
    search_window_hours: int = 3,
) -> list[SlotSuggestion]:
    """
    Returns alternative time slots on the same date within ±search_window_hours.
    Only returns slots with enough capacity for `guests`.
    Sorted by available capacity DESC.
    Generates candidates every 30 minutes.
    """
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant:
        return []

    base = datetime.combine(booking_date, preferred_time)
    candidates: list[time] = []

    for delta_minutes in range(-search_window_hours * 60, search_window_hours * 60 + 1, 30):
        if delta_minutes == 0:
            continue  # skip the exact time they already chose
        candidate_dt = base + timedelta(minutes=delta_minutes)
        candidate_t  = candidate_dt.time()

        # Respect restaurant opening hours if set
        if restaurant.opening_time and candidate_t < restaurant.opening_time:
            continue
        if restaurant.closing_time and candidate_t > restaurant.closing_time:
            continue
        # Don't suggest past times for today
        if booking_date == date.today() and candidate_t < datetime.now().time():
            continue

        candidates.append(candidate_t)

    results: list[SlotSuggestion] = []
    seen = set()

    for slot_time in candidates:
        # De-duplicate slots that fall in the same window
        window_key = slot_time.hour * 2 + (slot_time.minute // 30)
        if window_key in seen:
            continue
        seen.add(window_key)

        booked    = await _booked_in_window(db, restaurant_id, booking_date, slot_time)
        available = max(restaurant.max_capacity - booked, 0)
        rate      = booked / restaurant.max_capacity if restaurant.max_capacity else 0.0

        if available >= guests:  # only suggest if enough room
            results.append(SlotSuggestion(
                booking_time   = slot_time,
                available      = available,
                occupancy_rate = round(rate, 3),
                label          = _occupancy_label(rate),
            ))

    # Sort: least busy first
    results.sort(key=lambda s: s.occupancy_rate)
    return results[:6]  # max 6 suggestions


async def suggest_dates(
    db: AsyncSession,
    restaurant_id: int,
    preferred_date: date,
    preferred_time: time,
    guests: int,
    search_days: int = 7,
) -> list[DateSuggestion]:
    """
    Returns alternative dates within ±search_days where the same time slot
    has enough capacity for `guests`.
    """
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant:
        return []

    results: list[DateSuggestion] = []

    # Search forward first, then backward (users prefer future dates)
    offsets = sorted(
        [i for i in range(1, search_days + 1)] +
        [-i for i in range(1, search_days + 1)],
        key=lambda x: (abs(x), -x)   # nearest first, future preferred
    )

    for offset in offsets:
        candidate_date = preferred_date + timedelta(days=offset)
        if candidate_date < date.today():
            continue  # never suggest past dates

        booked    = await _booked_in_window(db, restaurant_id, candidate_date, preferred_time)
        available = max(restaurant.max_capacity - booked, 0)
        rate      = booked / restaurant.max_capacity if restaurant.max_capacity else 0.0

        if available >= guests:
            results.append(DateSuggestion(
                booking_date   = candidate_date,
                booking_time   = preferred_time,
                available      = available,
                occupancy_rate = round(rate, 3),
            ))

        if len(results) >= 5:
            break

    return results


async def get_restaurant_heatmap(
    db: AsyncSession,
    restaurant_id: int,
) -> dict[str, int]:
    """
    Returns historical booking counts by hour for a restaurant.
    Used to render a peak-hour heatmap in the UI.
    Format: { "10": 5, "12": 8, "18": 42, "19": 67, ... }
    """
    result = await db.execute(
        select(
            func.extract("hour", Booking.booking_time).label("hour"),
            func.sum(Booking.number_of_guests).label("total_guests"),
        )
        .where(
            and_(
                Booking.restaurant_id == restaurant_id,
                Booking.status        != BookingStatus.cancelled,
            )
        )
        .group_by(text("hour"))
        .order_by(text("hour"))
    )
    return {str(int(row.hour)): int(row.total_guests) for row in result.all()}