from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.bookings import router as booking_router
from app.api.v1.endpoints.user import router as user_router
app = FastAPI(title="Restaurant Booking API")

@app.get("/")
def read_root():
    return {"message": "Chào mừng bạn đến với hệ thống đặt bàn!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}




app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Cho phép Frontend này truy cập
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(booking_router, prefix="/api/v1/bookings", tags=["Bookings"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
