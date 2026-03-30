# app/core/exception_handlers.py
"""
Global exception handlers.
Registered once in main.py — applies to every endpoint uniformly.
Maps both domain exceptions and FastAPI/Pydantic exceptions
to the standard ErrorResponse envelope.
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions import (
    RestaurantNotFound,
    CapacityExceeded,
    TimeSlotConflict,
    BookingNotFound,
    InvalidBookingStatus,
)


def _error(code: str, message: str, detail: str | None = None, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "detail": detail,
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:

    # ── Domain exceptions ────────────────────────────────────────────

    @app.exception_handler(RestaurantNotFound)
    async def restaurant_not_found_handler(request: Request, exc: RestaurantNotFound):
        return _error("RESTAURANT_NOT_FOUND", "Không tìm thấy nhà hàng", status_code=404)

    @app.exception_handler(BookingNotFound)
    async def booking_not_found_handler(request: Request, exc: BookingNotFound):
        return _error("BOOKING_NOT_FOUND", "Không tìm thấy đơn đặt bàn hoặc bạn không có quyền", status_code=404)

    @app.exception_handler(TimeSlotConflict)
    async def timeslot_conflict_handler(request: Request, exc: TimeSlotConflict):
        return _error("TIMESLOT_CONFLICT", "Khung giờ này đã kín chỗ", status_code=409)

    @app.exception_handler(CapacityExceeded)
    async def capacity_exceeded_handler(request: Request, exc: CapacityExceeded):
        return _error(
            "CAPACITY_EXCEEDED",
            f"Nhà hàng không đủ chỗ. Còn trống: {exc.available} khách",
            detail=f"max_capacity={exc.max_capacity}, available={exc.available}",
            status_code=400,
        )

    @app.exception_handler(InvalidBookingStatus)
    async def invalid_status_handler(request: Request, exc: InvalidBookingStatus):
        return _error(
            "INVALID_STATUS",
            f"Trạng thái không hợp lệ: '{exc.value}'",
            detail="Giá trị hợp lệ: pending, confirmed, cancelled",
            status_code=422,
        )

    # ── Pydantic validation errors (422) ─────────────────────────────

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        # Flatten Pydantic errors into a readable list
        errors = []
        for err in exc.errors():
            loc = " → ".join(str(l) for l in err["loc"] if l != "body")
            errors.append(f"{loc}: {err['msg']}" if loc else err["msg"])

        return _error(
            "VALIDATION_ERROR",
            "Dữ liệu không hợp lệ",
            detail="; ".join(errors),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    # ── HTTPException passthrough (keep existing behavior) ───────────

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Map common status codes to error codes
        code_map = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
            409: "CONFLICT",
            422: "UNPROCESSABLE",
            429: "RATE_LIMITED",
            500: "INTERNAL_ERROR",
        }
        code = code_map.get(exc.status_code, "HTTP_ERROR")
        return _error(code, str(exc.detail), status_code=exc.status_code)