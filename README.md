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
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   │           ├── auth.py              # Đăng ký / Đăng nhập, create-admin-temp
│   │   │           ├── users.py             # Profile, đổi mật khẩu
│   │   │           ├── bookings.py          # Đặt bàn CRUD + /stats endpoint
│   │   │           ├── restaurants.py       # CRUD nhà hàng
│   │   │           └── admin.py             # Admin: stats, bookings, users
│   │   ├── core/
│   │   │   ├── config.py                    # Pydantic settings
│   │   │   ├── security.py                  # JWT, password hash
│   │   │   └── database.py                  # Async DB session
│   │   ├── models/
│   │   │   ├── base.py                      # DeclarativeBase
│   │   │   ├── user.py                      # + role, is_active, relationship
│   │   │   ├── restaurant.py                # Model nhà hàng
│   │   │   ├── booking.py                   # + restaurant_id FK, special_notes
│   │   │   └── __init__.py                  # Import đủ 3 models
│   │   ├── schemas/
│   │   │   ├── auth.py                      # Login, Register schemas
│   │   │   ├── user.py                      # UserRead, UserUpdate
│   │   │   ├── booking.py                   # + restaurant_id, special_notes
│   │   │   └── restaurant.py                # RestaurantRead/Create/Update
│   │   ├── services/
│   │   │   └── auth_service.py              # Business logic auth
│   │   ├── utils/
│   │   │   └── (các file utils nếu có)
│   │   ├── deps.py                          # + get_current_admin()
│   │   └── main.py                          # + restaurants, admin routers
│   ├── migrations/                          # Thư mục migrations (thay cho alembic/versions)
│   │   └── versions/                        # 4 migration files
│   ├── tests/
│   │   └── (các file test)
│   ├── .env                                 # Local config
│   ├── alembic.ini                          # Config migration
│   ├── requirements.txt                     # Dependencies
│   └── start.sh                             # Script khởi động Render
│
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── axios.js                     # + interceptor tự gắn token
    │   ├── components/
    │   │   └── (các component dùng chung)
    │   ├── router/
    │   │   └── index.js                     # + admin routes + guard
    │   ├── services/
    │   │   ├── auth.service.js              # + lưu user_role sau login
    │   │   └── booking.service.js
    │   ├── stores/
    │   │   ├── auth.js                      # Auth store (Pinia/Vuex)
    │   │   └── booking.js                   # Booking store
    │   └── views/
    │       ├── auth/
    │       │   ├── LoginView.vue            # + redirect theo role
    │       │   └── RegisterView.vue
    │       ├── booking/
    │       │   ├── DashboardView.vue        # + stats cards, apiClient
    │       │   ├── BookingCreateView.vue    # Chọn nhà hàng từ API
    │       │   └── BookingEditView.vue      # + info nhà hàng readonly
    │       ├── home/
    │       │   └── HomeView.vue             # Trang giới thiệu hoàn chỉnh
    │       ├── user/
    │       │   └── UserProfileView.vue      # + 5 stats, apiClient
    │       └── admin/                       # Admin views
    │           ├── AdminLayout.vue          # Sidebar + Topbar
    │           ├── AdminDashboard.vue       # Tổng quan số liệu
    │           ├── AdminRestaurants.vue     # CRUD nhà hàng
    │           ├── AdminBookings.vue        # Xác nhận booking
    │           └── AdminUsers.vue           # Quản lý user
    ├── .env.production                      # VITE_API_BASE_URL → Render
    ├── package.json
    └── vercel.json                          # Rewrite rules cho Vue Router
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

### System

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Root |
| GET | `/health` | Health check |


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
