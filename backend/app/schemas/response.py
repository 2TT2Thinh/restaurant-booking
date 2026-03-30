# app/schemas/response.py
"""
Standardized API response envelope.

All list endpoints return:
{
    "data": [...],
    "meta": { "total": 100, "skip": 0, "limit": 20, "page": 1, "pages": 5 }
}

All single-object endpoints return:
{
    "data": { ... }
}

All error responses return:
{
    "error": {
        "code": "RESTAURANT_NOT_FOUND",
        "message": "Không tìm thấy nhà hàng",
        "detail": null
    }
}
"""
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, computed_field
import math

T = TypeVar("T")


class Meta(BaseModel):
    total: int
    skip: int
    limit: int

    @computed_field
    @property
    def page(self) -> int:
        if self.limit == 0:
            return 1
        return (self.skip // self.limit) + 1

    @computed_field
    @property
    def pages(self) -> int:
        if self.limit == 0:
            return 1
        return max(1, math.ceil(self.total / self.limit))

    @computed_field
    @property
    def has_next(self) -> bool:
        return self.skip + self.limit < self.total

    @computed_field
    @property
    def has_prev(self) -> bool:
        return self.skip > 0


class PagedResponse(BaseModel, Generic[T]):
    """Envelope for paginated list responses."""
    data: List[T]
    meta: Meta

    @classmethod
    def create(cls, items: List[T], total: int, skip: int, limit: int) -> "PagedResponse[T]":
        return cls(
            data=items,
            meta=Meta(total=total, skip=skip, limit=limit),
        )


class DataResponse(BaseModel, Generic[T]):
    """Envelope for single-object responses."""
    data: T

    @classmethod
    def create(cls, item: T) -> "DataResponse[T]":
        return cls(data=item)


class ErrorDetail(BaseModel):
    code: str                          # Machine-readable: "CAPACITY_EXCEEDED"
    message: str                       # Human-readable: "Nhà hàng không đủ chỗ"
    detail: Optional[str] = None       # Optional extra context


class ErrorResponse(BaseModel):
    """Envelope for all error responses."""
    error: ErrorDetail

    @classmethod
    def create(cls, code: str, message: str, detail: Optional[str] = None) -> "ErrorResponse":
        return cls(error=ErrorDetail(code=code, message=message, detail=detail))