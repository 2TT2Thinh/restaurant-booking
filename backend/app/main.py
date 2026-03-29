from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.bookings import router as booking_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.restaurants import router as restaurant_router  # THÊM
from app.api.v1.endpoints.admin import router as admin_router
from app.core.config import settings
app = FastAPI(title="Restaurant Booking API")

# MIDDLEWARE phải đặt TRƯỚC include_router
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:5173"],
    allow_origins=settings.ALLOWED_ORIGINS,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Chào mừng bạn đến với hệ thống đặt bàn!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(booking_router, prefix="/api/v1/bookings", tags=["Bookings"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(restaurant_router, prefix="/api/v1/restaurants", tags=["Restaurants"])  
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])


