# 🍽️ Restaurant Booking System

Hệ thống đặt bàn nhà hàng trực tuyến xây dựng với **FastAPI** + **Vue 3 / Vuetify** + **PostgreSQL**.

Tính năng AI: **Recommendation Engine** (gợi ý nhà hàng, tính điểm dựa trên gu sở thích, độ tin cậy nhà hàng, phổ biến) +  **Chatbot** (hỏi đáp + intent detection).
## 🎯 Project Highlights

- **Full-stack application** with Vue 3 + FastAPI + PostgreSQL
- **AI-powered features**:
  - Recommendation engine (cuisine affinity + reliability + popularity + availability)
  - Chatbot with intent detection (recommend, availability, general chat via Ollama)
- **Role-based access control** (Customer / Admin) with JWT authentication
- **Real-time availability checking** & smart alternative suggestions
- **Production deployed**: Vercel (FE) + Render (BE + PostgreSQL)
- **Clean architecture**: Async SQLAlchemy, Pydantic validation, Alembic migrations

🌐 **Demo:** [restaurant-booking-bice.vercel.app](https://restaurant-booking-bice.vercel.app)  
📡 **API Docs:** [restaurant-booking-api-sj8b.onrender.com/docs](https://restaurant-booking-api-sj8b.onrender.com/docs)


---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    🖥️ FRONTEND (Vue 3 + Vuetify)               │
│  • Authentication Pages (Login/Register)                        │
│  • Booking Views (Search, Create, Edit, Cancel)                │
│  • Admin Dashboard (Stats, Bookings, Users, Restaurants)       │
│  • Chatbot Widget (Real-time AI Assistant)                    │
│  • User Profile (Info, Stats, Change Password)                │
└─────────────────────────────────────────────────────────────────┘
                         ↕ HTTP/REST (Axios)
┌─────────────────────────────────────────────────────────────────┐
│                 ⚡ BACKEND API (FastAPI)                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🔐 Auth         🍽️ Restaurants    📅 Bookings         │   │
│  │ - Login         - CRUD List       - CRUD List          │   │
│  │ - Register      - Search/Filter   - Search/Filter      │   │
│  │ - Change Pass   - Admin Mgmt      - Status Updates     │   │
│  │                                                         │   │
│  │ ⭐ Recommendations  💡 Smart Booking   🤖 Chatbot      │   │
│  │ - Pure SQL       - Slot Check       - Intent Detection │   │
│  │ - Scoring Algo   - Alt Dates        - LLM Integration │   │
│  │ - Cuisine Affinity - Alt Times      - Ollama Support  │   │
│  │                                                         │   │
│  │ 👨‍💼 Admin Routes    🔒 Security                          │
│  │ - Stats          - JWT Auth                            │   │
│  │ - Manage Users   - Role-Based Access (RBAC)           │   │
│  │ - Manage All     - Bcrypt Password Hash               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ⚙️ Core Services:                                              │
│  • auth_service.py         → Authentication Logic              │
│  • chatbot_service.py      → NLP + Intent Detection           │
│  • recommendation_service.py → ML Scoring Algorithm            │
│  • smart_booking_service.py → Availability Suggestions        │
└─────────────────────────────────────────────────────────────────┘
                         ↕ SQLAlchemy ORM
┌─────────────────────────────────────────────────────────────────┐
│                   💾 PostgreSQL Database                        │
│  • users (email, password, role, is_active)                   │
│  • restaurants (name, cuisine, capacity, hours)               │
│  • bookings (user_id, restaurant_id, date, status)            │
└─────────────────────────────────────────────────────────────────┘
                         ↕ REST API
┌─────────────────────────────────────────────────────────────────┐
│              🧠 Ollama LLM (llama3:latest)                      │
│  • Local AI Inference                                           │
│  • No External API Calls                                        │
│  • Used for General Chatbot Queries                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Main User Flows

### 1️⃣ **Authentication Flow** 🔐
```
User Login (email, password)
  → Password Verify (Bcrypt)
  → Generate JWT Token (HS256, 30min expiry)
  → Store in localStorage
  → Attach Authorization header to all requests
```

### 2️⃣ **Booking Flow** 📅
```
User Selects Restaurant + Date/Time
  → POST /bookings (create booking)
  → Backend checks availability
  
  IF slot available:
    → Create with status=pending
    → Admin reviews (PATCH)
    → Status → confirmed/cancelled
  
  IF slot full:
    → Suggest alternative dates (GET /suggestions/dates)
    → Suggest alternative times (GET /suggestions/times)
    → User reschedules
```

### 3️⃣ **Recommendation Flow** ⭐
```
User: "Gợi ý nhà hàng"
  → GET /recommendations/restaurants
  → Pure SQL Scoring Algorithm:
    • 40% Cuisine Affinity (based on past bookings)
    • 30% Restaurant Reliability (confirmed / total bookings)
    • 20% Weekly Popularity (booking volume last 7 days)
    • 10% Availability Today (remaining capacity)
  → Rank by weighted score
  → Return top 5 recommendations
```

### 4️⃣ **Chatbot Flow** 🤖
```
User Message → POST /chat
  → Intent Detection:
    • "recommend" → get_recommendations()
    • "availability" → check_slots()
    • "greeting" → return greeting
    • "times/dates" → suggest alternatives
    • "general" → call Ollama LLM
  → Format response
  → Return { data: "..." }
  → Frontend renders in chat UI
```

### 5️⃣ **Admin Dashboard** 👨‍💼
```
Admin Login (role=admin)
  → Verify RBAC
  → Access Dashboard:
    • Stats: Total bookings, pending, confirmed, cancelled
    • Bookings table: Search, filter by status, approve/reject
    • User management: Assign roles, activate/deactivate
    • Restaurant management: Add, edit, delete restaurants
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Vue 3 + Vuetify 3 | UI Components & Styling |
| **State** | Pinia | Global State Management |
| **HTTP** | Axios | API Client with Interceptors |
| **Build** | Vite | Fast Frontend Bundler |
| **Backend** | FastAPI | REST API Framework |
| **ORM** | SQLAlchemy (async) | Database Abstraction |
| **Database** | PostgreSQL 14+ | Primary Data Storage |
| **Auth** | JWT + Bcrypt | Security & Hashing |
| **Migrations** | Alembic | Schema Versioning |
| **Validation** | Pydantic | Request/Response Schemas |
| **AI** | Ollama (llama3:latest) | Local LLM for Chatbot |
| **Async** | asyncpg | PostgreSQL Async Driver |

---

## 📁 Project Structure

```
restaurant-booking/
│
├── frontend/                           # Vue 3 + Vuetify Application
│   ├── src/
│   │   ├── views/                     # Page Components
│   │   │   ├── auth/
│   │   │   │   ├── LoginView.vue
│   │   │   │   └── RegisterView.vue
│   │   │   ├── booking/
│   │   │   │   ├── DashboardView.vue
│   │   │   │   ├── BookingCreateView.vue
│   │   │   │   └── BookingEditView.vue
│   │   │   ├── user/
│   │   │   │   └── UserProfileView.vue
│   │   │   └── admin/
│   │   │       ├── AdminDashboard.vue
│   │   │       ├── AdminBookings.vue
│   │   │       ├── AdminUsers.vue
│   │   │       └── AdminRestaurants.vue
│   │   │
│   │   ├── components/                # Reusable UI Components
│   │   │   ├── Chatbot.vue            # 🤖 AI Assistant
│   │   │   └── common/
│   │   │
│   │   ├── services/                  # API Calls
│   │   │   ├── auth.service.js        # Authentication
│   │   │   ├── booking.service.js     # Bookmark Operations
│   │   │   ├── chatbot.service.js     # Chatbot API (⭐)
│   │   │   └── axios.js               # HTTP Interceptor
│   │   │
│   │   ├── stores/                    # Pinia Global State
│   │   │   ├── auth.js                # User & Token State
│   │   │   └── booking.js             # Booking State
│   │   │
│   │   ├── api/
│   │   │   └── axios.js               # Axios Client Config
│   │   │
│   │   ├── router/
│   │   │   └── index.js               # Route Definitions
│   │   │
│   │   ├── App.vue
│   │   └── main.js
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── backend/                            # FastAPI Application
│   ├── app/
│   │   ├── main.py                    # App Entry Point
│   │   │
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/         # Route Handlers
│   │   │   │   │   ├── auth.py        # 🔐 Login/Register
│   │   │   │   │   ├── restaurants.py # 🍽️ CRUD Restaurants
│   │   │   │   │   ├── bookings.py    # 📅 User Bookings
│   │   │   │   │   ├── user.py        # 👤 User Profile
│   │   │   │   │   ├── chatbot.py     # 🤖 Chat Endpoint (⭐)
│   │   │   │   │   ├── recommendations.py  # ⭐ Recommendations
│   │   │   │   │   ├── suggestions.py      # 💡 Smart Booking
│   │   │   │   │   └── admin.py       # 👨‍💼 Admin Routes
│   │   │   │   │
│   │   │   │   └── deps.py            # Dependencies (Auth, DB)
│   │   │   │
│   │   │   └── exception_handlers.py  # Global Error Handlers
│   │   │
│   │   ├── core/
│   │   │   ├── config.py              # Settings & Env Vars
│   │   │   ├── security.py            # JWT & Bcrypt Utils
│   │   │   └── exception_handlers.py  # Error Handling
│   │   │
│   │   ├── services/                  # Business Logic (⭐ AI)
│   │   │   ├── auth_service.py        # User Authentication
│   │   │   ├── chatbot_service.py     # 🤖 NLP + Intent Detection
│   │   │   ├── recommendation_service.py # ⭐ ML Scoring
│   │   │   └── smart_booking_service.py  # 💡 Availability
│   │   │
│   │   ├── models/                    # SQLAlchemy ORM Models
│   │   │   ├── user.py                # User Table
│   │   │   ├── booking.py             # Booking Table
│   │   │   └── restaurant.py          # Restaurant Table
│   │   │
│   │   ├── schemas/                   # Pydantic Models
│   │   │   ├── auth.py                # Login/Register
│   │   │   ├── booking.py             # Booking Data
│   │   │   ├── response.py            # Response Wrappers
│   │   │   └── restaurant.py          # Restaurant Data
│   │   │
│   │   ├── crud/                      # Database Queries (if needed)
│   │   │   ├── crud_booking.py
│   │   │   └── crud_restaurant.py
│   │   │
│   │   └── db/
│   │       └── session.py             # DB Connection Pool
│   │
│   ├── alembic/                       # Database Migrations
│   │   ├── env.py
│   │   └── versions/
│   │       ├── c5009f86d970_initial_migration...py
│   │       ├── 56a95498e586_add_role_to_user.py
│   │       ├── 7ab8230e69d5_add_restaurant_table.py
│   │       └── ... (more migrations)
│   │
│   ├── .env.example                   # Environment Template
│   ├── requirements.txt                # Python Dependencies
│   ├── alembic.ini                    # Alembic Config
│   └── start.sh                       # Deployment Script
│
├── DEPLOYMENT.md                      # 🚀 Complete Deploy Guide
├── README.md                          # This file
├── .gitignore                         # Git Ignore Rules
└── package.json (root)                # Monorepo Config
```

---

## ✨ Key Features

### User Features
- ✅ **Registration & Authentication:** Email-based signup, JWT login (30min expiry)
- ✅ **Booking Management:** Create, reschedule, cancel bookings with real-time status
- ✅ **Smart Recommendations:** AI-powered restaurant suggestions based on cuisine preference, reliability, popularity
- ✅ **Chatbot Assistant:** Ask questions, get restaurant recommendations, check availability
- ✅ **Profile Management:** View booking history, update info, change password

### Admin Features
- ✅ **Dashboard:** Real-time statistics (total bookings, pending, confirmed, cancelled)
- ✅ **Booking Management:** Approve/reject bookings, delete bookings
- ✅ **Restaurant Management:** Add, edit, delete restaurants with capacity & hours
- ✅ **User Management:** Assign admin roles, activate/deactivate accounts
- ✅ **Advanced Search:** Filter bookings by status, restaurant, date

### AI & ML Features
- ⭐ **Recommendation Engine:** 
  - 40% Cuisine Affinity (past preferences)
  - 30% Restaurant Reliability (success rate)
  - 20% Weekly Popularity (booking volume)
  - 10% Availability Today (remaining capacity)
- 🤖 **Chatbot with Intent Detection:**
  - `recommend` → Get AI recommendations
  - `availability` → Check restaurant availability
  - `greeting` → Friendly responses
  - `times/dates` → Suggest alternatives
  - `general` → Call Ollama LLM for questions

---

## 🔒 Security

| Aspect | Implementation |
|--------|-----------------|
| **Authentication** | JWT (HS256), 30-minute expiry |
| **Password** | Bcrypt hashing (12 rounds) |
| **Authorization** | Role-Based Access Control (RBAC: customer, admin) |
| **CORS** | Restricted to frontend URL only |
| **HTTPS** | Enforced in production (nginx redirect) |
| **SQL Injection** | Protected via SQLAlchemy ORM + Parameterized Queries |
| **XSS** | Vue 3 auto-escaping + CSP headers (production) |
| **CSRF** | CORS + Same-site cookies |
| **Secrets** | Environment variables (.env NOT in git) |
| **Rate Limiting** | Optional (slowapi middleware) |

---

## 📊 API Response Format

All endpoints return **unified envelope format**:

### ✅ Single Object Response
```json
{
  "data": {
    "id": 1,
    "name": "Phở Hà Nội",
    "cuisine_type": "Việt Nam"
  }
}
```

### ✅ List Response (Admin)
```json
{
  "data": [
    {"id": 1, "name": "..."},
    {"id": 2, "name": "..."}
  ]
}
```

### ✅ Pagination Response
```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "skip": 0,
    "limit": 20,
    "page": 1,
    "pages": 5
  }
}
```

### ❌ Error Response
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Nhà hàng không tìm thấy",
    "detail": null
  }
}
```

### 🤖 Chatbot Response Format
```json
{
  "data": "🍽️ Gợi ý nhà hàng dành cho bạn:\n1. Nhà hàng Sen Vàng (Việt Nam)\n2. Sushi Tokyo (Nhật Bản)",
  "intent": "recommend",
  "processing_time_ms": 123
}
```
Frontend lấy nội dung bằng: response.data.data

---

## 🔌 API Endpoints

### Authentication 🔐
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new account |
| POST | `/api/v1/auth/login` | Login → JWT token |

### Users 👤
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users/me` | Get profile info |
| PATCH | `/api/v1/users/me` | Update profile |
| GET | `/api/v1/users/me/stats` | User booking stats |
| POST | `/api/v1/users/me/change-password` | Change password |

### Bookings 📅
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/bookings/stats` | Booking statistics |
| GET | `/api/v1/bookings/me` | My bookings list |
| POST | `/api/v1/bookings/` | Create new booking |
| PATCH | `/api/v1/bookings/{id}` | Update/reschedule booking |
| DELETE | `/api/v1/bookings/{id}` | Cancel booking |

### Restaurants 🍽️
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/restaurants/` | List restaurants (searchable) |
| GET | `/api/v1/restaurants/{id}` | Restaurant details |
| POST | `/api/v1/restaurants/` | Create restaurant (Admin) |
| PATCH | `/api/v1/restaurants/{id}` | Update restaurant (Admin) |
| DELETE | `/api/v1/restaurants/{id}` | Delete restaurant (Admin) |

### Recommendations ⭐ (AI)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/recommendations/restaurants` | Get top 5 recommendations |

### Smart Booking 💡 (AI)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/suggestions/slot` | Kiểm tra slot còn trống |
| GET | `/api/v1/suggestions/times` | Gợi ý khung giờ thay thế |
| GET | `/api/v1/suggestions/dates` | Gợi ý ngày thay thế |
| GET | `/api/v1/suggestions/heatmap/{id}` | Biểu đồ giờ cao điểm |

### Chatbot 🤖 (AI)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/v1/chat/` | Gửi tin nhắn chatbot |
| GET | `/api/v1/chat/health` | Kiểm tra health |
| GET | `/api/v1/chat/intents` | Danh sách intent hỗ trợ |

### Admin 👨‍💼
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/admin/stats` | Dashboard statistics |
| GET | `/api/v1/admin/bookings` | All bookings (paginated) |
| PATCH | `/api/v1/admin/bookings/{id}` | Approve/reject booking |
| DELETE | `/api/v1/admin/bookings/{id}` | Delete booking |
| GET | `/api/v1/admin/users` | List all users |
| PATCH | `/api/v1/admin/users/{id}` | Change user role/status |

---

## 📋 Requirements

Before starting, ensure you have:

- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [PostgreSQL 14+](https://www.postgresql.org/download/)
- [Ollama](https://ollama.ai/) (for chatbot) - optional
- Git

---

## 🚀 Installation & Setup

### Step 1 — Clone Repository

```bash
git clone https://github.com/your-repo/restaurant-booking.git
cd restaurant-booking
```

---

### Step 2 — Create PostgreSQL Database

Open PostgreSQL (psql or pgAdmin) and run:

```sql
CREATE DATABASE restaurant_booking;
CREATE USER booking_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE restaurant_booking TO booking_user;
```

> Customize database name, user, and password as needed (must match `.env` later).

---

### Step 3 — Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create `backend/.env`:

```env
DATABASE_URL=postgresql+asyncpg://booking_user:secure_password@localhost:5432/restaurant_booking
SECRET_KEY=your_32_char_min_random_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
FRONTEND_URL=http://localhost:5173
ENVIRONMENT=development
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL_NAME=llama3:latest
INTERNAL_BASE_URL=http://localhost:8000/api/v1
```

Run migrations:

```bash
alembic upgrade head
```

Start backend:

```bash
uvicorn app.main:app --reload --port 8000
```

> API Docs: http://localhost:8000/docs

---

### Step 4 — Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install
```

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Start frontend:

```bash
npm run dev
```

> Frontend: http://localhost:5173

---

### Step 5 — Setup Ollama (Optional - for Chatbot)

```bash
# Download & install Ollama from https://ollama.ai
# Pull llama3 model
ollama pull llama3:latest

# Run Ollama service
ollama serve
```

> Port: http://localhost:11434

---

### Step 6 — Create Admin Account

1. Go to http://localhost:5173/register
2. Create an account with your email
3. Open PostgreSQL and run:

```sql
UPDATE users SET role = 'admin' WHERE email = 'your@email.com';
```

4. Refresh page and access `/admin/dashboard`

---

## 🧪 Testing

### Test Endpoints with Swagger UI

```
http://localhost:8000/docs
```

### Test Chatbot

```bash
# Send chat message
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"gợi ý nhà hàng"}]}'
```

### Test Recommendations

```bash
curl http://localhost:8000/api/v1/recommendations/restaurants \
  -H "Authorization: Bearer <token>"
```

---

## 🚀 Deployment

See **[DEPLOYMENT.md](./DEPLOYMENT.md)** for complete deployment guide:
- Render.com setup (recommended for quick deploy)
- Docker + Heroku
- AWS/GCP/Azure setup
- Pre-deployment checklist

### Quick Deploy to Render

1. Push to GitHub (ensure `.env` NOT committed)
2. Create Render Web Service from repo
3. Set environment variables
4. Deploy!

---

## 📝 Environment Variables

See `.env.example` files:

**Backend (.env.example):**
- `DATABASE_URL` - PostgreSQL connection
- `SECRET_KEY` - JWT secret (32+ chars)
- `ENVIRONMENT` - development|production
- `OLLAMA_HOST` - Ollama API endpoint
- `FRONTEND_URL` - Frontend domain for CORS

**Frontend (.env.example):**
- `VITE_API_BASE_URL` - Backend API URL

---

## 🔧 Development

### Run Tests

```bash
cd backend
pytest tests/
```

### Format Code

```bash
black app/
isort app/
```

### Type Checking

```bash
mypy app/
```

---

## 📚 Tech Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Vue 3 Docs](https://vuejs.org/)
- [Vuetify 3 Docs](https://vuetifyjs.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [Ollama](https://ollama.ai/)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 📞 Support

For issues and questions:
- Open GitHub Issues
- Check existing documentation
- Review DEPLOYMENT.md for production help

---

**Last Updated:** April 2, 2026  
**Version:** 1.0.0  
**Status:** ✅ Production Ready


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
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/
│   │   │   ├── auth.py          # Đăng ký / Đăng nhập
│   │   │   ├── users.py         # Profile, đổi mật khẩu
│   │   │   ├── bookings.py      # Đặt bàn CRUD + stats
│   │   │   ├── restaurants.py   # CRUD nhà hàng
│   │   │   └── admin.py         # Admin endpoints
│   │   ├── core/
│   │   │   ├── config.py        # Pydantic settings
│   │   │   ├── security.py      # JWT, password hash
│   │   │   └── database.py      # Async DB session
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── crud/                # Database operations
│   │   ├── services/            # Business logic
│   │   └── main.py
│   ├── alembic/                 # Migration files
│   ├── .env                     # Local config (không commit)
│   ├── alembic.ini
│   ├── requirements.txt
│   └── start.sh                 # Script deploy Render
│
└── frontend/
    ├── src/
    │   ├── api/axios.js          # Axios + interceptor
    │   ├── router/index.js       # Routes + guard
    │   ├── services/
    │   │   └── auth.service.js
    │   └── views/
    │       ├── auth/             # Login, Register
    │       ├── booking/          # Dashboard, Create, Edit
    │       ├── home/             # Landing page
    │       ├── user/             # Profile
    │       └── admin/            # Admin panel
    ├── .env                      # Local config (không commit)
    ├── .env.production           # Production config
    ├── vercel.json               # Deploy config
    └── package.json
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
