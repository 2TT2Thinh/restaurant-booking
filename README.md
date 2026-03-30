# 🍽️ Restaurant Booking System

Hệ thống đặt bàn nhà hàng trực tuyến xây dựng với **FastAPI** + **Vue 3 / Vuetify**.

🌐 **Demo:** [restaurant-booking-bice.vercel.app](https://restaurant-booking-bice.vercel.app)  
📡 **API Docs:** [restaurant-booking-api-sj8b.onrender.com/docs](https://restaurant-booking-api-sj8b.onrender.com/docs)

---

## 🛠 Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy (Async), Alembic, PostgreSQL, JWT |
| Frontend | Vue 3, Vuetify 3, Vue Router, Axios |

---

## ✨ Tính năng

- **Auth:** Đăng ký, đăng nhập JWT. Phân quyền `customer` / `admin`
- **Booking:** Tạo, sửa, hủy, xóa đặt bàn. Filter theo trạng thái và tìm kiếm
- **Restaurants:** Xem danh sách nhà hàng, chọn khi đặt bàn
- **Profile:** Xem thống kê booking, cập nhật thông tin, đổi mật khẩu
- **Admin Panel:** Quản lý nhà hàng, booking, user với sidebar dashboard

---

## 📋 Yêu cầu

Trước khi bắt đầu, cần cài đặt:

- [Python 3.12+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [PostgreSQL 14+](https://www.postgresql.org/download/)
- Git

---

## 🚀 Cài đặt & Chạy Local

### Bước 1 — Clone repo

```bash
git clone https://github.com/2TT2Thinh/restaurant-booking.git
cd restaurant-booking
```

---

### Bước 2 — Tạo Database PostgreSQL

Mở PostgreSQL (psql hoặc pgAdmin) và chạy:

```sql
CREATE DATABASE restaurant_booking;
CREATE USER booking_user WITH PASSWORD '123456';
GRANT ALL PRIVILEGES ON DATABASE restaurant_booking TO booking_user;
```

> Bạn có thể đặt tên database, user, password khác — miễn là khớp với file `.env` ở bước sau.

---

### Bước 3 — Setup Backend

```bash
cd backend

# Tạo môi trường ảo
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (Linux/Mac)
source venv/bin/activate

# Cài dependencies
pip install -r requirements.txt
```

Tạo file `backend/.env`:

```env
DATABASE_URL=postgresql://booking_user:123456@localhost:5432/restaurant_booking
SECRET_KEY=cc5d98d5dd828ae44daea1b2e6b60ad96153bdd394d143a4b68400b4261e9c98
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:5173
ENVIRONMENT=development
```

> ⚠️ Thay `booking_user`, `123456`, `restaurant_booking` nếu bạn dùng tên khác ở Bước 2.

Chạy migration để tạo bảng:

```bash
alembic upgrade head
```

> Nếu thành công sẽ thấy log như:
> ```
> INFO [alembic.runtime.migration] Running upgrade -> c5009f86d970, Initial migration...
> INFO [alembic.runtime.migration] Running upgrade ... -> 56a95498e586, add role to user
> ```

Khởi động server:

```bash
uvicorn app.main:app --reload --port 8000
```

> API docs: **http://localhost:8000/docs**

---

### Bước 4 — Setup Frontend

```bash
cd ../frontend

# Cài dependencies
npm install
```

Tạo file `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Chạy frontend:

```bash
npm run dev
```

> Chạy tại: **http://localhost:5173**

---

### Bước 5 — Tạo tài khoản Admin

Sau khi backend đang chạy, vào **http://localhost:8000/docs**:

1. Gọi **POST /api/v1/auth/register** để tạo tài khoản
2. Vào PostgreSQL, chạy lệnh:

```sql
UPDATE users SET role = 'admin' WHERE email = 'your@email.com';
```

Hoặc dùng pgAdmin 4 → Tools → Query Tool → chạy lệnh trên.

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/v1/auth/register` | Đăng ký tài khoản |
| POST | `/api/v1/auth/login` | Đăng nhập → JWT token |

### Users
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/users/me` | Thông tin profile |
| PATCH | `/api/v1/users/me` | Cập nhật profile |
| GET | `/api/v1/users/me/stats` | Thống kê booking |
| POST | `/api/v1/users/me/change-password` | Đổi mật khẩu |

### Bookings
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/bookings/stats` | Thống kê booking |
| GET | `/api/v1/bookings/me` | Danh sách booking của tôi |
| POST | `/api/v1/bookings/` | Tạo booking mới |
| PATCH | `/api/v1/bookings/{id}` | Sửa / hủy booking |
| DELETE | `/api/v1/bookings/{id}` | Xóa booking |

### Restaurants
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/restaurants/` | Danh sách nhà hàng |
| GET | `/api/v1/restaurants/{id}` | Chi tiết nhà hàng |
| POST | `/api/v1/restaurants/` | Tạo nhà hàng (Admin) |
| PATCH | `/api/v1/restaurants/{id}` | Sửa nhà hàng (Admin) |
| DELETE | `/api/v1/restaurants/{id}` | Xóa nhà hàng (Admin) |

### Admin
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/admin/stats` | Thống kê tổng quan |
| GET | `/api/v1/admin/bookings` | Tất cả booking |
| PATCH | `/api/v1/admin/bookings/{id}` | Xác nhận / hủy booking |
| GET | `/api/v1/admin/users` | Danh sách user |
| PATCH | `/api/v1/admin/users/{id}` | Đổi role / kích hoạt user |

---

## 🗂️ Cấu trúc dự án

```
restaurant-booking/
├── backend/ # FastAPI Backend
│ ├── alembic/ # Database migrations
│ ├── app/
│ │ ├── api/v1/endpoints/ # API endpoints
│ │ │ ├── auth.py
│ │ │ ├── bookings.py
│ │ │ ├── chatbot.py
│ │ │ ├── recommendations.py
│ │ │ ├── restaurants.py
│ │ │ └── user.py
│ │ ├── core/ # Config & security
│ │ ├── crud/ # CRUD operations
│ │ ├── models/ # SQLAlchemy models
│ │ ├── schemas/ # Pydantic schemas
│ │ └── services/ # Business logic
│ │ ├── auth_service.py
│ │ ├── chatbot_service.py
│ │ ├── recommendation_service.py
│ │ └── smart_booking_service.py
│ ├── requirements.txt
│ └── .env
│
└── frontend/ # Vue 3 Frontend
├── src/
│ ├── api/ # API calls
│ ├── components/ # Vue components
│ ├── router/ # Vue Router
│ ├── services/ # Service layer
│ ├── stores/ # Pinia stores
│ └── views/ # Page views
│ ├── admin/ # Admin pages
│ ├── auth/ # Login/Register
│ ├── booking/ # Booking pages
│ ├── home/ # Home page
│ └── user/ # User profile
├── package.json
└── vite.config.js
```

---

## ☁️ Deploy

| Service | Platform | Link |
|---------|----------|------|
| Frontend | Vercel | [restaurant-booking-bice.vercel.app](https://restaurant-booking-bice.vercel.app) |
| Backend | Render | [restaurant-booking-api-sj8b.onrender.com](https://restaurant-booking-api-sj8b.onrender.com) |
| Database | Render PostgreSQL | — |

---

## 🤝 Đóng góp

```bash
git checkout -b feature/ten-tinh-nang
git commit -m "feat: mô tả thay đổi"
git push origin feature/ten-tinh-nang
# Mở Pull Request
```

---

## 📄 Giấy phép

MIT License
