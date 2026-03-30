# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.bookings import router as booking_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.restaurants import router as restaurant_router
from app.api.v1.endpoints.admin import router as admin_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: add init logic here (e.g. warm cache, verify DB connection)
    yield
    # Shutdown: clean up resources if needed


app = FastAPI(
    title="Restaurant Booking API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# ── Middleware (must be before routers) ──────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global exception handlers ────────────────────────────────────────────────
register_exception_handlers(app)

# ── Routes ───────────────────────────────────────────────────────────────────
app.include_router(auth_router,       prefix="/api/v1/auth",        tags=["Authentication"])
app.include_router(booking_router,    prefix="/api/v1/bookings",     tags=["Bookings"])
app.include_router(user_router,       prefix="/api/v1/users",        tags=["Users"])
app.include_router(restaurant_router, prefix="/api/v1/restaurants",  tags=["Restaurants"])
app.include_router(admin_router,      prefix="/api/v1/admin",        tags=["Admin"])


@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "Chào mừng bạn đến với hệ thống đặt bàn!"}


@app.get("/health", include_in_schema=False)
def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}