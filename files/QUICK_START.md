# ⚡ QUICK START - 5 PHÚT

Hướng dẫn siêu nhanh để chạy project ngay lập tức.

## 🎯 Prerequisites (Cài sẵn rồi)

- Python 3.11+
- PostgreSQL 15+
- Node.js 18+

## 🚀 BACKEND (2 phút)

```bash
cd backend

# 1. Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install
pip install -r requirements.txt

# 3. Environment
cp .env.example .env
# Edit .env: DATABASE_URL, SECRET_KEY, GOOGLE_MAPS_API_KEY

# 4. Database
createdb restaurant_booking
alembic upgrade head

# 5. Run
uvicorn app.main:app --reload
```

✅ Backend chạy tại: http://localhost:8000
📚 API Docs: http://localhost:8000/docs

## 🎨 FRONTEND (2 phút)

```bash
# Mở terminal mới
cd frontend

# 1. Install
npm install

# 2. Environment
cp .env.example .env
# Edit .env: VITE_API_BASE_URL=http://localhost:8000

# 3. Run
npm run dev
```

✅ Frontend chạy tại: http://localhost:5173

## 🧪 TEST (1 phút)

1. Mở http://localhost:5173
2. Click "Register"
3. Tạo account mới
4. Auto redirect về My Bookings
5. Click "New Booking" → Tạo booking
6. Done! ✨

## ⚠️ Gặp lỗi?

Xem **SETUP_GUIDE.md** để troubleshooting chi tiết.

## 📦 File Structure

```
restaurant-booking/
├── backend/          # FastAPI + PostgreSQL
├── frontend/         # Vue 3 + Vuetify
├── README.md         # Full documentation
└── SETUP_GUIDE.md    # Detailed setup guide
```

## 🎓 Next Steps

1. Đọc README.md để hiểu project
2. Explore API docs tại /docs
3. Customize theo ý thích
4. Deploy lên Railway + Vercel

---

**Happy Coding! 🚀**
