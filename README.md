# 🍽️ Restaurant Booking System

> **Hệ thống đặt bàn nhà hàng trực tuyến tích hợp AI**  
> Full-stack online restaurant booking system with AI-powered features
<img width="1834" height="924" alt="image" src="https://github.com/user-attachments/assets/f75b3bc3-08e8-47e9-8c58-15eb1100a049" />
<img width="1915" height="917" alt="image" src="https://github.com/user-attachments/assets/c3f5d138-23db-41bf-9bb5-8c9d4c18e389" />
<img width="1911" height="897" alt="image" src="https://github.com/user-attachments/assets/1c2bfa01-077c-4d4a-9cfc-09b3a83169e2" />
<img width="1920" height="893" alt="image" src="https://github.com/user-attachments/assets/6496d1af-c154-48b2-b5ef-6c919241695e" />
<img width="1920" height="967" alt="image" src="https://github.com/user-attachments/assets/9ef49547-43fc-4e66-bdca-c8c41b2abd08" />
<img width="439" height="687" alt="image" src="https://github.com/user-attachments/assets/468cc754-a35f-4590-90f7-64633e601b75" />
<img width="1920" height="893" alt="image" src="https://github.com/user-attachments/assets/0256eb2e-b416-49a5-b44a-fb80f246c9f0" />



---

**🌐 Live Demo:** [restaurant-booking-bice.vercel.app](https://restaurant-booking-bice.vercel.app)  
**📡 API Docs:** [restaurant-booking-api-sj8b.onrender.com/docs](https://restaurant-booking-api-sj8b.onrender.com/docs)  
**📦 GitHub:** [github.com/2TT2Thinh/restaurant-booking](https://github.com/2TT2Thinh/restaurant-booking)

---

## ✨ Project Highlights / Điểm nổi bật

- 🔐 **JWT Authentication** with role-based access control (Customer / Admin)
- ⭐ **AI Recommendation Engine** — scores restaurants by cuisine affinity (40%), reliability (30%), popularity (20%), availability (10%)
- 🤖 **AI Chatbot** with intent detection (recommend, availability, general chat via Ollama/llama3)
- 💡 **Smart Booking** — real-time slot checking + alternative date/time suggestions
- 👨‍💼 **Admin Dashboard** — manage bookings, users, restaurants with statistics
- 🚀 **Production deployed** on Vercel (frontend) + Render (backend + PostgreSQL)
- 🏗️ **Clean architecture** — Async SQLAlchemy, Pydantic validation, Alembic migrations

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Vue 3 + Vuetify 3 | UI Components & Styling |
| State | Pinia | Global State Management |
| HTTP | Axios | API Client with Interceptors |
| Build | Vite | Fast Frontend Bundler |
| Backend | FastAPI | REST API Framework |
| ORM | SQLAlchemy (async) | Database Abstraction |
| Database | PostgreSQL 14+ | Primary Data Storage |
| Auth | JWT + Bcrypt | Security & Password Hashing |
| Migrations | Alembic | Schema Versioning |
| Validation | Pydantic | Request/Response Schemas |
| AI | Ollama (llama3:latest) | Local LLM for Chatbot |
| Async Driver | asyncpg | PostgreSQL Async Driver |
| Deploy | Vercel + Render | Frontend + Backend Hosting |

---

## 📊 System Architecture

```
┌──────────────────────────────────────────────────┐
│           🖥️ FRONTEND (Vue 3 + Vuetify)          │
│  Auth · Booking · Admin Dashboard · Chatbot      │
└──────────────────┬───────────────────────────────┘
                   │ HTTP/REST (Axios)
┌──────────────────▼───────────────────────────────┐
│            ⚡ BACKEND API (FastAPI)               │
│                                                  │
│  🔐 Auth   🍽️ Restaurants   📅 Bookings         │
│  ⭐ Recommendations   💡 Smart Booking           │
│  🤖 Chatbot (Intent Detection)                   │
│  👨‍💼 Admin Routes   🔒 RBAC Security              │
└──────────────────┬───────────────────────────────┘
                   │ SQLAlchemy ORM
┌──────────────────▼───────────────────────────────┐
│            💾 PostgreSQL Database                │
│  users · restaurants · bookings                 │
└──────────────────┬───────────────────────────────┘
                   │ REST API
┌──────────────────▼───────────────────────────────┐
│         🧠 Ollama LLM (llama3:latest)            │
│  Local AI inference — no external API calls      │
└──────────────────────────────────────────────────┘
```

---

## 🎯 Key User Flows / Luồng chính

### 1. Recommendation Engine ⭐
```
User requests recommendations
  → Pure SQL Scoring Algorithm:
     • 40% Cuisine Affinity    (based on past bookings)
     • 30% Restaurant Reliability (confirmed / total bookings)
     • 20% Weekly Popularity   (booking volume last 7 days)
     • 10% Availability Today  (remaining capacity)
  → Return top 5 ranked restaurants
```

### 2. Smart Booking 💡
```
User selects restaurant + date/time
  → Check slot availability
  IF available  → Create booking (status: pending) → Admin approval
  IF full       → Suggest alternative dates/times → User reschedules
```

### 3. Chatbot 🤖
```
User message → Intent Detection:
  "recommend"    → get_recommendations()
  "availability" → check_slots()
  "greeting"     → return greeting
  "times/dates"  → suggest alternatives
  "general"      → call Ollama LLM
```

---

## 🔒 Security

| Aspect | Implementation |
|--------|---------------|
| Authentication | JWT (HS256), 30-minute expiry |
| Password | Bcrypt hashing (12 rounds) |
| Authorization | Role-Based Access Control (customer, admin) |
| CORS | Restricted to frontend URL only |
| SQL Injection | SQLAlchemy ORM + parameterized queries |
| XSS | Vue 3 auto-escaping |
| Secrets | Environment variables (`.env` not in git) |

---

## 🔌 API Endpoints

<details>
<summary><strong>Authentication 🔐</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new account |
| POST | `/api/v1/auth/login` | Login → JWT token |

</details>

<details>
<summary><strong>Bookings 📅</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/bookings/me` | My bookings list |
| POST | `/api/v1/bookings/` | Create new booking |
| PATCH | `/api/v1/bookings/{id}` | Update / reschedule |
| DELETE | `/api/v1/bookings/{id}` | Cancel booking |

</details>

<details>
<summary><strong>AI Features ⭐🤖</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/recommendations/restaurants` | Top 5 AI recommendations |
| POST | `/api/v1/chat/` | Send chatbot message |
| GET | `/api/v1/suggestions/dates` | Alternative date suggestions |
| GET | `/api/v1/suggestions/times` | Alternative time suggestions |
| GET | `/api/v1/suggestions/heatmap/{id}` | Peak hours heatmap |

</details>

<details>
<summary><strong>Admin 👨‍💼</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/admin/stats` | Dashboard statistics |
| GET | `/api/v1/admin/bookings` | All bookings (paginated) |
| PATCH | `/api/v1/admin/bookings/{id}` | Approve / reject booking |
| GET | `/api/v1/admin/users` | List all users |
| PATCH | `/api/v1/admin/users/{id}` | Change role / status |

</details>

---

## 📁 Project Structure / Cấu trúc dự án

```
restaurant-booking/
├── frontend/                   # Vue 3 + Vuetify
│   └── src/
│       ├── views/              # Pages: auth, booking, admin, user
│       ├── components/         # Chatbot.vue, common/
│       ├── services/           # API service layer
│       ├── stores/             # Pinia: auth, booking
│       └── router/
│
├── backend/                    # FastAPI
│   └── app/
│       ├── api/v1/endpoints/   # auth, bookings, restaurants,
│       │                       # chatbot, recommendations, admin
│       ├── services/           # Business logic + AI
│       │   ├── chatbot_service.py
│       │   ├── recommendation_service.py
│       │   └── smart_booking_service.py
│       ├── models/             # SQLAlchemy ORM
│       ├── schemas/            # Pydantic
│       ├── core/               # Config, security, JWT
│       └── db/
│
├── alembic/                    # Database migrations
├── DEPLOYMENT.md
└── README.md
```

---

## 🚀 Getting Started / Cài đặt

### Prerequisites / Yêu cầu

- Python 3.12+
- Node.js 18+
- PostgreSQL 14+
- Git
- Ollama *(optional, for chatbot)*

### 1. Clone the repository

```bash
git clone https://github.com/2TT2Thinh/restaurant-booking.git
cd restaurant-booking
```

### 2. Setup PostgreSQL database

```sql
CREATE DATABASE restaurant_booking;
CREATE USER booking_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE restaurant_booking TO booking_user;
```

### 3. Setup Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

Create `backend/.env`:

```env
DATABASE_URL=postgresql+asyncpg://booking_user:your_secure_password@localhost:5432/restaurant_booking
SECRET_KEY=your_random_secret_key_minimum_32_characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:5173
ENVIRONMENT=development
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL_NAME=llama3:latest
INTERNAL_BASE_URL=http://localhost:8000/api/v1
```

```bash
alembic upgrade head
uvicorn app.main:app --reload --port 8000
# API Docs: http://localhost:8000/docs
```

### 4. Setup Frontend

```bash
cd ../frontend
npm install
```

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

```bash
npm run dev
# Frontend: http://localhost:5173
```

### 5. Setup Ollama *(optional)*

```bash
# Install from https://ollama.ai
ollama pull llama3:latest
ollama serve
```

### 6. Create Admin account

```bash
# Register via http://localhost:5173/register, then run:
UPDATE users SET role = 'admin' WHERE email = 'your@email.com';
```

---

## ☁️ Deployment / Deploy

| Service | Platform | URL |
|---------|----------|-----|
| Frontend | Vercel | [restaurant-booking-bice.vercel.app](https://restaurant-booking-bice.vercel.app) |
| Backend | Render | [restaurant-booking-api-sj8b.onrender.com](https://restaurant-booking-api-sj8b.onrender.com) |
| Database | Render PostgreSQL | — |

See [DEPLOYMENT.md](DEPLOYMENT.md) for full deployment guide.

---

## ⚠️ Known Limitations / Hạn chế

- Booking conflict handling is not fully covered
- Lack of unit tests and advanced validation
- UI is not fully responsive on all screen sizes
- Ollama requires local setup (not available in cloud demo)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built by [Nguyễn Tấn Thịnh](https://github.com/2TT2Thinh) · Last updated: April 2026*
