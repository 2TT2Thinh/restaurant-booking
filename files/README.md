# 🍽️ Restaurant Booking System

Hệ thống đặt chỗ nhà hàng đơn giản được xây dựng với FastAPI (Backend) và Vue 3 (Frontend) - Dự án thực tập sinh Backend.

## 📸 Screenshots

> _Thêm screenshots sau khi hoàn thành UI_

## ✨ Features

### Core Features
- ✅ **User Authentication**: Register, Login với JWT
- ✅ **Booking Management**: Create, Read, Update, Delete bookings
- ✅ **Google Maps Integration**: Geocode địa chỉ → lat/lng
- ✅ **Status Management**: Pending, Confirmed, Cancelled
- ✅ **Responsive UI**: Material Design với Vuetify

### Business Logic
- Validation booking date (không được quá khứ)
- Validation giờ mở cửa (9 AM - 10 PM)
- Check số lượng khách (1-50 người)
- User chỉ xem được bookings của mình

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3.11
- **Framework**: FastAPI 0.110+
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Auth**: JWT (python-jose)
- **Password Hash**: bcrypt (passlib)

### Frontend
- **Framework**: Vue 3 (Composition API)
- **UI Library**: Vuetify 3
- **State Management**: Pinia
- **HTTP Client**: Axios
- **Build Tool**: Vite

### Third-party APIs
- Google Maps Geocoding API

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Google Maps API Key

## 🚀 Quick Start

### 1. Clone repository

```bash
git clone <your-repo-url>
cd restaurant-booking
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env với database credentials và API keys

# Create database
createdb restaurant_booking

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

Backend sẽ chạy tại: `http://localhost:8000`

API Docs: `http://localhost:8000/docs`

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env với backend URL

# Start dev server
npm run dev
```

Frontend sẽ chạy tại: `http://localhost:5173`

## 📚 API Documentation

### Authentication Endpoints

```
POST /api/v1/auth/register   # Đăng ký user mới
POST /api/v1/auth/login      # Login và nhận JWT token
GET  /api/v1/auth/me         # Lấy thông tin user hiện tại
```

### Booking Endpoints

```
POST   /api/v1/bookings              # Tạo booking mới
GET    /api/v1/bookings              # Danh sách bookings (có filter)
GET    /api/v1/bookings/{id}         # Chi tiết booking
PUT    /api/v1/bookings/{id}         # Update booking
PUT    /api/v1/bookings/{id}/status  # Update trạng thái
DELETE /api/v1/bookings/{id}         # Xóa booking
```

### Geocoding Endpoint

```
POST /api/v1/geocode  # Convert địa chỉ → lat/lng
```

Chi tiết đầy đủ: http://localhost:8000/docs

## 🗄️ Database Schema

```sql
-- Users table
users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW()
)

-- Bookings table
bookings (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  restaurant_name VARCHAR(255) NOT NULL,
  restaurant_address TEXT,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  booking_date DATE NOT NULL,
  booking_time TIME NOT NULL,
  number_of_guests INTEGER NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)
```

## 📁 Project Structure

```
restaurant-booking/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Config & security
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── database.py
│   │   └── main.py
│   ├── alembic/           # Database migrations
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── views/         # Page components
│   │   ├── stores/        # Pinia stores
│   │   ├── services/      # API services
│   │   ├── router/        # Vue Router
│   │   └── plugins/       # Vuetify config
│   ├── package.json
│   └── .env
│
└── README.md
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Manual Testing

1. Đăng ký user mới
2. Login và nhận token
3. Tạo booking mới
4. Geocode địa chỉ
5. Xem danh sách bookings
6. Update status → cancelled
7. Delete booking

## 🚢 Deployment

### Backend - Railway.app

1. Tạo project mới
2. Add PostgreSQL database
3. Connect GitHub repository
4. Set environment variables
5. Deploy!

### Frontend - Vercel

1. Import GitHub repository
2. Framework preset: Vite
3. Add environment variables
4. Deploy!

## 🔒 Security Features

- ✅ Password hashing với bcrypt
- ✅ JWT token authentication
- ✅ CORS configuration
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input validation (Pydantic)
- ✅ Authorization checks (user can only access their own bookings)

## 🎯 Learning Objectives

Dự án này giúp học được:

1. **Backend Development**
   - RESTful API design
   - JWT authentication flow
   - Database modeling với relationships
   - Alembic migrations
   - Business logic validation

2. **Frontend Development**
   - Vue 3 Composition API
   - State management với Pinia
   - API integration với Axios
   - Material Design UI

3. **Full-stack Integration**
   - CORS handling
   - Token-based authentication
   - Error handling
   - Third-party API integration

## 📝 Git Workflow

```bash
# Feature branch
git checkout -b feature/booking-crud

# Commit với message rõ ràng
git commit -m "feat: add booking CRUD endpoints"

# Push và create PR
git push origin feature/booking-crud
```

## 🐛 Common Issues & Solutions

### Backend

**Issue**: `ModuleNotFoundError`
```bash
# Activate virtual environment
source venv/bin/activate
```

**Issue**: Database connection error
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Check DATABASE_URL in .env
```

### Frontend

**Issue**: API calls fail
```bash
# Check backend is running on port 8000
# Check CORS is configured correctly
```

## 📞 Support

Nếu gặp vấn đề:
1. Check logs trong terminal
2. Xem API docs tại /docs
3. Review code examples trong README

## 🎓 Next Steps (Optional Enhancements)

- [ ] Email notifications (SendGrid)
- [ ] Review & rating system
- [ ] Restaurant photos gallery
- [ ] Advanced filters
- [ ] Export bookings to CSV
- [ ] Unit tests coverage 80%+

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

[Your Name] - Backend Intern Portfolio Project

---

**⭐ Star this repo if you find it helpful!**
