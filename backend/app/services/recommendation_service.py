# app/services/recommendation_service.py
"""
Restaurant recommendation engine.
Pure SQL scoring — no external ML library required.
Run entirely in the existing PostgreSQL database.

Scoring formula (weights sum to 1.0):
  cuisine_affinity      0.40  — matches user's past cuisine preferences
  booking_success_rate  0.30  — restaurant reliability (confirmed / total)
  popularity_this_week  0.20  — recent booking volume (social proof)
  availability_score    0.10  — remaining capacity for today

Cold-start (new user with no bookings): falls back to
  popularity_this_week + booking_success_rate only.
"""
from datetime import date, timedelta
from typing import Optional

from sqlalchemy import func, select, case, and_, Float, cast
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, BookingStatus
from app.models.restaurant import Restaurant


# ── Weight constants (tune these without touching logic) ─────────────────────
W_CUISINE    = 0.40
W_SUCCESS    = 0.30
W_POPULARITY = 0.20
W_AVAIL      = 0.10


async def get_recommendations(
    db: AsyncSession,
    user_id: int,
    limit: int = 10,
    for_date: Optional[date] = None,
) -> list[dict]:
    """
    Returns a list of dicts:
      { restaurant: Restaurant, score: float, reason: str }
    sorted by score descending.
    """
    target_date = for_date or date.today()
    week_ago    = target_date - timedelta(days=7)

    # ── Step 1: Get user's cuisine affinity ──────────────────────────────────
    # Count bookings per cuisine for this user → normalize to 0–1
    cuisine_counts = await db.execute(
        select(
            Restaurant.cuisine_type,
            func.count(Booking.id).label("cnt"),
        )
        .join(Booking, Booking.restaurant_id == Restaurant.id)
        .where(Booking.user_id == user_id)
        .group_by(Restaurant.cuisine_type)
    )
    rows = cuisine_counts.all()
    total_user_bookings = sum(r.cnt for r in rows)
    # cuisine_type → affinity score (0.0–1.0)
    cuisine_affinity: dict[str, float] = {}
    if total_user_bookings > 0:
        for r in rows:
            cuisine_affinity[r.cuisine_type or ""] = r.cnt / total_user_bookings

    # ── Step 2: Score every restaurant in a single query ─────────────────────
    # Subquery: total and confirmed bookings per restaurant
    total_bookings_sq = (
        select(
            Booking.restaurant_id,
            func.count(Booking.id).label("total"),
            func.count(case((Booking.status == BookingStatus.confirmed, 1))).label("confirmed"),
        )
        .group_by(Booking.restaurant_id)
        .subquery()
    )

    # Subquery: bookings this week per restaurant
    week_bookings_sq = (
        select(
            Booking.restaurant_id,
            func.count(Booking.id).label("week_count"),
        )
        .where(
            and_(
                Booking.booking_date >= week_ago,
                Booking.booking_date <= target_date,
                Booking.status != BookingStatus.cancelled,
            )
        )
        .group_by(Booking.restaurant_id)
        .subquery()
    )

    # Subquery: booked guests today
    today_booked_sq = (
        select(
            Booking.restaurant_id,
            func.coalesce(func.sum(Booking.number_of_guests), 0).label("booked_today"),
        )
        .where(
            and_(
                Booking.booking_date == target_date,
                Booking.status != BookingStatus.cancelled,
            )
        )
        .group_by(Booking.restaurant_id)
        .subquery()
    )

    result = await db.execute(
        select(
            Restaurant,
            func.coalesce(total_bookings_sq.c.total,       0).label("total_bookings"),
            func.coalesce(total_bookings_sq.c.confirmed,   0).label("confirmed_bookings"),
            func.coalesce(week_bookings_sq.c.week_count,   0).label("week_count"),
            func.coalesce(today_booked_sq.c.booked_today,  0).label("booked_today"),
        )
        .outerjoin(total_bookings_sq, Restaurant.id == total_bookings_sq.c.restaurant_id)
        .outerjoin(week_bookings_sq,  Restaurant.id == week_bookings_sq.c.restaurant_id)
        .outerjoin(today_booked_sq,   Restaurant.id == today_booked_sq.c.restaurant_id)
    )
    all_rows = result.all()

    if not all_rows:
        return []

    # Normalize week_count across all restaurants (0–1)
    max_week = max((r.week_count for r in all_rows), default=1) or 1

    scored = []
    for row in all_rows:
        restaurant: Restaurant = row.Restaurant

        # Cuisine affinity (0–1)
        affinity = cuisine_affinity.get(restaurant.cuisine_type or "", 0.0)
        # If new user → equal affinity for all (cold start)
        if total_user_bookings == 0:
            affinity = 0.5

        # Success rate (0–1): confirmed / total, default 1.0 if no history
        if row.total_bookings > 0:
            success = row.confirmed_bookings / row.total_bookings
        else:
            success = 1.0  # benefit of the doubt for new restaurants

        # Popularity (0–1): normalized week count
        popularity = row.week_count / max_week

        # Availability (0–1): remaining capacity / max_capacity
        remaining   = max(restaurant.max_capacity - row.booked_today, 0)
        availability = remaining / restaurant.max_capacity if restaurant.max_capacity else 0.5

        score = (
            affinity    * W_CUISINE
            + success   * W_SUCCESS
            + popularity * W_POPULARITY
            + availability * W_AVAIL
        )

        # Human-readable reason for the top signal
        reason = _build_reason(affinity, success, popularity, availability, total_user_bookings)

        scored.append({
            "restaurant":  restaurant,
            "score":       round(score, 4),
            "reason":      reason,
            "available_seats": remaining,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]


def _build_reason(
    affinity: float, success: float, popularity: float,
    availability: float, user_booking_count: int
) -> str:
    """Returns the single strongest reason for the recommendation."""
    if user_booking_count == 0:
        return "Phổ biến trong tuần này"
    if affinity >= 0.4:
        return "Phù hợp với sở thích ẩm thực của bạn"
    if success >= 0.85:
        return "Tỷ lệ xác nhận đặt bàn cao"
    if popularity >= 0.7:
        return "Được đặt nhiều trong tuần này"
    if availability >= 0.8:
        return "Còn nhiều chỗ trống hôm nay"
    return "Gợi ý cho bạn"