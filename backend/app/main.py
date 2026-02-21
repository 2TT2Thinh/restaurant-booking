from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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