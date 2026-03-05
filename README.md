# 🍽️ Restaurant Booking System

Hệ thống đặt bàn nhà hàng trực tuyến xây dựng với **FastAPI** + **Vue 3 / Vuetify**.

---

## 🛠 Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy (Async), Alembic, PostgreSQL, JWT |
| Frontend | Vue 3, Vuetify 3, Pinia, Vue Router, Axios |

---

## 📁 Cấu trúc dự án

```
restaurant-booking/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/
│   │   │   ├── auth.py          # Đăng ký / Đăng nhập
│   │   │   ├── users.py         # Profile, đổi mật khẩu
│   │   │   ├── restaurants.py   # Quản lý nhà hàng
│   │   │   └── bookings.py      # Đặt bàn CRUD
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py      # JWT, password hash
│   │   │   └── database.py      # Async DB session
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   ├── utils/
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   ├── .env
│   ├── alembic.ini
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── api/axios.js
    │   ├── components/
    │   ├── router/index.js
    │   ├── services/
    │   │   ├── auth.service.js
    │   │   └── booking.service.js
    │   ├── stores/
    │   │   ├── auth.js
    │   │   └── booking.js
    │   └── views/
    │       ├── auth/            # Login, Register
    │       ├── booking/         # Dashboard, Create, Edit
    │       ├── home/
    │       └── user/            # Profile
    └── package.json
```

---

## 🚀 Cài đặt

### Backend

```bash
cd backend
python3 -m venv venv && source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

Tạo file `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/restaurant_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

```bash
# Windows
venv\Scripts\activate
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

> API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
```

Tạo file `.env`:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

```bash
npm run dev
```

> Chạy tại: http://localhost:5173

---

## 🔌 API Endpoints

### Auth — `/api/v1/auth`

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/login` | Đăng nhập → trả về JWT token |
| POST | `/register` | Tạo tài khoản mới |

### Users — `/api/v1/users`

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/me` | Lấy thông tin profile |
| GET | `/me/stats` | Thống kê đặt bàn của user |
| PATCH | `/me` | Cập nhật họ tên, số điện thoại |
| POST | `/me/change-password` | Đổi mật khẩu |

### Restaurants — `/api/v1/restaurants`

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Danh sách nhà hàng |
| POST | `/` | Tạo nhà hàng mới |
| GET | `/{id}` | Chi tiết nhà hàng |
| PUT | `/{id}` | Cập nhật nhà hàng |
| DELETE | `/{id}` | Xóa nhà hàng |

### Bookings — `/api/v1/bookings`

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/me` | Danh sách đặt bàn (filter: `search`, `status`, `skip`, `limit`) |
| POST | `/` | Tạo đặt bàn mới — `user_id` lấy tự động từ token |
| PATCH | `/{id}` | Cập nhật hoặc hủy đặt bàn |
| DELETE | `/{id}` | Xóa vĩnh viễn đặt bàn |

---

## ✨ Tính năng

- **Auth:** Đăng ký, đăng nhập với JWT. Mật khẩu được hash bcrypt.
- **Profile:** Xem và cập nhật thông tin cá nhân, đổi mật khẩu an toàn.
- **Bookings:** Tạo, sửa, hủy, xóa đặt bàn. Filter theo trạng thái và từ khóa.
- **Restaurants:** CRUD đầy đủ danh sách nhà hàng.
- **Async:** Toàn bộ backend dùng `async/await` với SQLAlchemy async session.

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
