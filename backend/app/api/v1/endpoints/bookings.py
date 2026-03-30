# app/api/v1/endpoints/bookings.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.api import deps
from app.crud import crud_booking
from app.schemas.booking import BookingCreate, BookingRead, BookingUpdate
from app.schemas.response import PagedResponse, DataResponse
from app.models.user import User
from app.exceptions import (
    BookingNotFound,
    CapacityExceeded,
    RestaurantNotFound,
    TimeSlotConflict,
)

router = APIRouter()


@router.get("/stats")
async def get_my_stats(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return await crud_booking.get_booking_stats(db, user_id=current_user.id)


@router.get("/me", response_model=PagedResponse[BookingRead])
async def read_my_bookings(
    search: Optional[str] = None,
    status: Optional[str] = None,
    skip: int  = Query(default=0,  ge=0),
    limit: int = Query(default=20, le=100),
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    items, total = await crud_booking.get_multi_bookings(
        db=db,
        user_id=current_user.id,
        search=search,
        status=status,
        skip=skip,
        limit=limit,
    )
    return PagedResponse.create(items=items, total=total, skip=skip, limit=limit)


@router.post("/", response_model=DataResponse[BookingRead], status_code=status.HTTP_201_CREATED)
async def create_new_booking(
    booking_in: BookingCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # Domain exceptions are caught by global handlers in exception_handlers.py
    booking = await crud_booking.create_booking(
        db=db, obj_in=booking_in, user_id=current_user.id
    )
    return DataResponse.create(booking)


@router.patch("/{booking_id}", response_model=DataResponse[BookingRead])
async def update_existing_booking(
    booking_id: int,
    booking_in: BookingUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    booking = await crud_booking.update_booking(
        db=db,
        booking_id=booking_id,
        obj_in=booking_in,
        user_id=current_user.id,
    )
    return DataResponse.create(booking)


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_booking(
    booking_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    await crud_booking.delete_booking(
        db=db, booking_id=booking_id, user_id=current_user.id
    )
    return None