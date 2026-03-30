# app/api/v1/endpoints/recommendations.py
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.api import deps
from app.models.user import User
from app.schemas.restaurant import RestaurantRead
from app.services.recommendation_service import get_recommendations

router = APIRouter()


class RecommendationItem(BaseModel):
    restaurant:      RestaurantRead
    score:           float
    reason:          str          # human-readable label shown in UI
    available_seats: int

    model_config = {"from_attributes": True}


class RecommendationResponse(BaseModel):
    data: list[RecommendationItem]
    meta: dict                    # could include user_booking_count, date


@router.get("/restaurants", response_model=RecommendationResponse)
async def recommend_restaurants(
    for_date: Optional[date] = Query(default=None, description="YYYY-MM-DD. Defaults to today."),
    limit: int = Query(default=5, le=20),
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Returns ranked restaurant recommendations for the current user.
    Factors in: cuisine preferences, restaurant reliability,
    weekly popularity, and today's availability.
    """
    results = await get_recommendations(
        db=db,
        user_id=current_user.id,
        limit=limit,
        for_date=for_date,
    )

    items = [
        RecommendationItem(
            restaurant=r["restaurant"],
            score=r["score"],
            reason=r["reason"],
            available_seats=r["available_seats"],
        )
        for r in results
    ]

    return RecommendationResponse(
        data=items,
        meta={"date": str(for_date or date.today()), "count": len(items)},
    )