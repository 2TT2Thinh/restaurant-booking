# 🚀 HƯỚNG DẪN SETUP CHI TIẾT - TỪNG BƯỚC

Guide này sẽ hướng dẫn bạn setup project từ đầu, phù hợp cho người mới bắt đầu.

## 📋 CHECKLIST YÊU CẦU

Trước khi bắt đầu, đảm bảo bạn đã cài đặt:

- [ ] Python 3.11+ (`python --version`)
- [ ] PostgreSQL 15+ (`psql --version`)
- [ ] Node.js 18+ (`node --version`)
- [ ] npm (`npm --version`)
- [ ] Git (`git --version`)

## 🔧 PHẦN 1: SETUP BACKEND (30-45 phút)

### Bước 1: Clone và chuẩn bị

```bash
# Clone repository (hoặc tạo folder mới)
mkdir restaurant-booking
cd restaurant-booking

# Copy toàn bộ code backend vào folder này
```

### Bước 2: Tạo virtual environment

```bash
cd backend

# Tạo virtual environment
python -m venv venv

# Activate virtual environment
# Trên Windows:
venv\Scripts\activate

# Trên Mac/Linux:
source venv/bin/activate

# Sau khi activate, terminal sẽ hiển thị (venv) ở đầu dòng
```

### Bước 3: Install dependencies

```bash
# Đảm bảo bạn đang ở folder backend/
pip install -r requirements.txt

# Kiểm tra installation
pip list
```

### Bước 4: Setup PostgreSQL Database

#### Option A: PostgreSQL đã cài sẵn

```bash
# Mở PostgreSQL terminal
psql -U postgres

# Trong psql terminal:
CREATE DATABASE restaurant_booking;
CREATE USER booking_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE restaurant_booking TO booking_user;
\q
```

#### Option B: Cài PostgreSQL mới

**Windows:**
1. Download PostgreSQL từ: https://www.postgresql.org/download/windows/
2. Chạy installer, nhớ password cho user `postgres`
3. Tạo database như Option A

**Mac (với Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
createdb restaurant_booking
```

**Linux (Ubuntu):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb restaurant_booking
```

### Bước 5: Tạo Google Maps API Key

1. Truy cập: https://console.cloud.google.com/
2. Tạo project mới hoặc chọn project existing
3. Enable **Geocoding API**
4. Create credentials → API Key
5. Copy API key

### Bước 6: Configure Environment Variables

```bash
# Tạo file .env từ example
cp .env.example .env

# Mở .env và chỉnh sửa:
nano .env  # hoặc code .env
```

File `.env` của bạn:

```env
# Database - THAY ĐỔI CHO PHỚP HỢP
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/restaurant_booking

# JWT Secret - GENERATE MỚI
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Maps API
GOOGLE_MAPS_API_KEY=your-actual-google-maps-api-key

# CORS
FRONTEND_URL=http://localhost:5173

# Environment
ENVIRONMENT=development
```

**Tạo SECRET_KEY mới:**
```bash
# Trên Mac/Linux:
openssl rand -hex 32

# Trên Windows (dùng Python):
python -c "import secrets; print(secrets.token_hex(32))"
```

### Bước 7: Run Database Migrations

```bash
# Kiểm tra Alembic config
alembic current

# Tạo initial migration
alembic revision --autogenerate -m "Initial migration with users and bookings"

# Áp dụng migration
alembic upgrade head

# Verify migration đã chạy
alembic current
```

### Bước 8: Start Backend Server

```bash
# Development mode (auto-reload)
uvicorn app.main:app --reload

# Hoặc
python -m app.main
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Bước 9: Test Backend API

Mở browser và truy cập:
- http://localhost:8000 → Thấy welcome message
- http://localhost:8000/docs → Swagger UI (API documentation)

**Test API với Swagger:**
1. Mở http://localhost:8000/docs
2. Thử endpoint `POST /api/v1/auth/register`
3. Click "Try it out"
4. Nhập data:
```json
{
  "email": "test@example.com",
  "password": "test123456",
  "full_name": "Test User",
  "phone": "0123456789"
}
```
5. Click "Execute"
6. Kiểm tra Response → 201 Created ✅

---

## 🎨 PHẦN 2: SETUP FRONTEND (20-30 phút)

### Bước 1: Install Node Modules

```bash
# Mở terminal mới (giữ backend terminal chạy)
cd frontend

# Install dependencies
npm install

# Nếu gặp error, thử:
npm install --legacy-peer-deps
```

### Bước 2: Configure Environment

```bash
# Tạo .env từ example
cp .env.example .env

# Chỉnh sửa .env
code .env
```

File `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

### Bước 3: Start Frontend Dev Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### Bước 4: Test Frontend

1. Mở browser: http://localhost:5173
2. Bạn sẽ thấy trang Login
3. Click "Don't have an account? Register"
4. Đăng ký tài khoản mới
5. Sau khi đăng ký → auto redirect về My Bookings page

---

## ✅ VERIFICATION CHECKLIST

### Backend ✅
- [ ] Server chạy tại http://localhost:8000
- [ ] API docs accessible tại /docs
- [ ] Database connection thành công
- [ ] Có thể register user mới qua Swagger
- [ ] Có thể login và nhận JWT token

### Frontend ✅
- [ ] App chạy tại http://localhost:5173
- [ ] Trang Login hiển thị đúng
- [ ] Có thể đăng ký user mới
- [ ] Có thể login
- [ ] Redirect đúng sau login

### Integration ✅
- [ ] Frontend có thể call Backend API
- [ ] CORS không báo error
- [ ] JWT token được lưu vào localStorage
- [ ] Protected routes hoạt động

---

## 🐛 TROUBLESHOOTING

### Backend Issues

**1. `ModuleNotFoundError: No module named 'app'`**
```bash
# Đảm bảo bạn đang ở folder backend/
pwd

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

**2. `sqlalchemy.exc.OperationalError: could not connect to server`**
```bash
# Kiểm tra PostgreSQL đang chạy
# Mac:
brew services list

# Linux:
sudo service postgresql status

# Windows:
# Services → PostgreSQL → Start

# Kiểm tra DATABASE_URL trong .env
cat .env | grep DATABASE_URL
```

**3. `alembic.util.exc.CommandError`**
```bash
# Xóa migrations cũ và tạo lại
rm -rf alembic/versions/*.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

**4. Port 8000 đã được sử dụng**
```bash
# Tìm process đang dùng port 8000
# Mac/Linux:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

**1. `Failed to fetch` khi gọi API**
- Kiểm tra backend đang chạy
- Kiểm tra VITE_API_BASE_URL trong .env
- Mở DevTools → Network tab → Xem error chi tiết

**2. CORS error**
```
Access to XMLHttpRequest blocked by CORS policy
```
- Kiểm tra FRONTEND_URL trong backend/.env
- Restart backend server
- Clear browser cache

**3. Vuetify components không hiển thị**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**4. `Module not found: Can't resolve '@/...'`**
```bash
# Restart dev server
# Ctrl+C để stop
npm run dev
```

### Database Issues

**1. Không thể tạo database**
```bash
# Check PostgreSQL user permissions
psql -U postgres
\du

# Grant superuser nếu cần
ALTER USER postgres WITH SUPERUSER;
```

**2. Migration conflict**
```bash
# Downgrade to base
alembic downgrade base

# Re-run migrations
alembic upgrade head
```

---

## 🎯 NEXT STEPS

Sau khi setup xong:

1. **Làm quen với codebase:**
   - Đọc backend/app/main.py
   - Xem API structure trong /api/v1/
   - Hiểu flow trong frontend/src/views/

2. **Test các features:**
   - Register → Login → Create Booking → View Bookings
   - Test geocoding với địa chỉ thật
   - Test cancel booking
   - Test delete booking

3. **Customize:**
   - Thay đổi màu theme trong frontend/src/plugins/vuetify.js
   - Thêm validation rules
   - Cải thiện UI

4. **Deploy:**
   - Push code lên GitHub
   - Deploy backend lên Railway
   - Deploy frontend lên Vercel

---

## 📚 HELPFUL COMMANDS

### Backend
```bash
# Activate venv
source venv/bin/activate

# Start server
uvicorn app.main:app --reload

# Create migration
alembic revision --autogenerate -m "message"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check current migration
alembic current
```

### Frontend
```bash
# Install deps
npm install

# Dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Git
```bash
# Initial commit
git init
git add .
git commit -m "Initial commit: Restaurant Booking System"

# Push to GitHub
git remote add origin <your-repo-url>
git push -u origin main
```

---

## 🎓 LEARNING RESOURCES

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Vue 3**: https://vuejs.org/guide/
- **Vuetify**: https://vuetifyjs.com/
- **Pinia**: https://pinia.vuejs.org/

---

**Chúc bạn setup thành công! 🚀**

Nếu gặp vấn đề không có trong guide này, mở issue trên GitHub hoặc check logs chi tiết.
