# app/api/v1/endpoints/suggestions.py
"""
Smart booking suggestion endpoints.
Called by the frontend BEFORE the user confirms a booking —
acts as a "pre-check" that gives real-time feedback.

Flow:
  1. User selects restaurant + date + time + guests
  2. Frontend calls GET /suggestions/slot  → shows occupancy badge
  3. If slot is peak → frontend calls GET /suggestions/times for alternatives
  4. If whole day is busy → frontend calls GET /suggestions/dates
  5. GET /suggestions/heatmap → rendered as a bar chart on restaurant detail page
"""
from datetime import date, time
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.api import deps
from app.models.user import User
from app.services.smart_booking_service import (
    SlotAnalysis,
    SlotSuggestion,
    DateSuggestion,
    analyze_slot,
    suggest_time_slots,
    suggest_dates,
    get_restaurant_heatmap,
)

router = APIRouter()


# ── Response schemas ─────────────────────────────────────────────────────────

class SlotAnalysisResponse(BaseModel):
    restaurant_id:  int
    booking_date:   date
    booking_time:   time
    max_capacity:   int
    booked_guests:  int
    available:      int
    occupancy_rate: float
    is_peak:        bool
    label:          str


class SlotSuggestionResponse(BaseModel):
    booking_time:   time
    available:      int
    occupancy_rate: float
    label:          str


class DateSuggestionResponse(BaseModel):
    booking_date:   date
    booking_time:   time
    available:      int
    occupancy_rate: float


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/slot", response_model=SlotAnalysisResponse)
async def check_slot(
    restaurant_id: int,
    booking_date:  date,
    booking_time:  time,
    guests:        int  = Query(default=1, ge=1),
    db: AsyncSession    = Depends(deps.get_db),
    current_user: User  = Depends(deps.get_current_user),
):
    """
    Analyze a specific slot before booking.
    Frontend uses this to show: 'Còn nhiều chỗ ✅' or 'Rất đông ⚠️' badge.
    """
    analysis = await analyze_slot(db, restaurant_id, booking_date, booking_time, guests)
    return SlotAnalysisResponse(**analysis.__dict__)


@router.get("/times", response_model=list[SlotSuggestionResponse])
async def suggest_times(
    restaurant_id: int,
    booking_date:  date,
    booking_time:  time,
    guests:        int  = Query(default=1, ge=1),
    db: AsyncSession    = Depends(deps.get_db),
    current_user: User  = Depends(deps.get_current_user),
):
    """
    Suggests alternative time slots on the same day.
    Call this when /slot returns is_peak=true.
    Returns up to 6 less-busy alternatives sorted by occupancy ascending.
    """
    suggestions = await suggest_time_slots(
        db, restaurant_id, booking_date, booking_time, guests
    )
    return [SlotSuggestionResponse(**s.__dict__) for s in suggestions]


@router.get("/dates", response_model=list[DateSuggestionResponse])
async def suggest_alternative_dates(
    restaurant_id: int,
    booking_date:  date,
    booking_time:  time,
    guests:        int  = Query(default=1, ge=1),
    db: AsyncSession    = Depends(deps.get_db),
    current_user: User  = Depends(deps.get_current_user),
):
    """
    Suggests alternative dates within ±7 days when today is fully booked.
    """
    suggestions = await suggest_dates(
        db, restaurant_id, booking_date, booking_time, guests
    )
    return [DateSuggestionResponse(**s.__dict__) for s in suggestions]


@router.get("/heatmap/{restaurant_id}", response_model=dict)
async def restaurant_heatmap(
    restaurant_id: int,
    db: AsyncSession   = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Returns historical booking volume by hour.
    { "10": 12, "18": 87, "19": 120 }
    Used to render a peak-hour bar chart on the restaurant detail page.
    No auth required in production — can be made public if needed.
    """
    return await get_restaurant_heatmap(db, restaurant_id)