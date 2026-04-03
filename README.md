# 🍽️ Restaurant Booking System

> A production-ready fullstack web application for online restaurant reservations — built with **FastAPI**, **Vue 3**, and **PostgreSQL**, featuring AI-powered recommendations and a smart chatbot assistant.

🌐 **Live Demo:** [restaurant-booking-bice.vercel.app](https://restaurant-booking-bice.vercel.app)  
📡 **API Docs:** [restaurant-booking-api-sj8b.onrender.com/docs](https://restaurant-booking-api-sj8b.onrender.com/docs)  
📦 **Repo:** [github.com/2TT2Thinh/restaurant-booking](https://github.com/2TT2Thinh/restaurant-booking)

---

## 🎯 What Problem Does It Solve?

Finding and booking a restaurant online is often fragmented — no smart suggestions, no real-time availability, and no help when your preferred slot is full. This system addresses all of that:

- Users get **personalized restaurant recommendations** based on their dining history
- When a slot is unavailable, the system **automatically suggests alternative times and dates**
- A **conversational chatbot** helps users explore options without navigating menus
- Admins get a **full dashboard** to manage bookings, users, and restaurants in one place

---

## ✨ Key Features & Impact

### 👤 For Users
- **Secure authentication** — JWT-based login with Bcrypt password hashing
- **Smart booking flow** — real-time slot checking with automatic fallback suggestions
- **AI recommendations** — personalized restaurant picks ranked by a weighted scoring algorithm
- **Chatbot assistant** — natural language interface for checking availability and getting suggestions
- **Profile & history** — view past bookings, update info, change password

### 👨‍💼 For Admins
- **Live dashboard** — total bookings, pending approvals, cancellations at a glance
- **Booking management** — approve, reject, or delete bookings with search and filtering
- **Restaurant management** — full CRUD for restaurant listings, capacity, and hours
- **User management** — assign roles, activate/deactivate accounts

---

## 🤖 AI & Smart Features

### ⭐ Recommendation Engine
A pure-SQL scoring algorithm ranks restaurants by relevance to each user:

| Factor | Weight | Description |
|--------|--------|-------------|
| Cuisine Affinity | 40% | Based on user's past booking history |
| Restaurant Reliability | 30% | Ratio of confirmed to total bookings |
| Weekly Popularity | 20% | Booking volume in the last 7 days |
| Today's Availability | 10% | Remaining capacity right now |

→ **Returns top 5 personalized recommendations**, no black-box ML required.

### 🤖 Chatbot with Intent Detection
The chatbot classifies messages into intents and responds accordingly:

- `recommend` → triggers the recommendation engine
- `availability` → checks real-time slot data
- `times / dates` → surfaces smart booking suggestions
- `greeting` → friendly acknowledgement
- `general` → routes to a local LLM (Ollama / llama3) for open-ended questions

---

## 🏗️ System Architecture

```
┌─────────────────────────────────┐
│   Frontend (Vue 3 + Vuetify)    │
│   Booking · Admin · Chatbot     │
└────────────┬────────────────────┘
             │ HTTP/REST (Axios)
┌────────────▼────────────────────┐
│      Backend API (FastAPI)      │
│                                 │
│  Auth · Bookings · Restaurants  │
│  Recommendations · Chatbot      │
│  Smart Booking · Admin          │
└────────────┬────────────────────┘
             │ SQLAlchemy (async)
┌────────────▼────────────────────┐
│       PostgreSQL Database       │
│  users · bookings · restaurants │
└─────────────────────────────────┘
             │ REST
┌────────────▼────────────────────┐
│    Ollama LLM (llama3:latest)   │
│    Local inference · No API key │
└─────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Vue 3, Vuetify 3, Pinia, Axios, Vite |
| **Backend** | FastAPI, SQLAlchemy (async), Pydantic, Alembic |
| **Database** | PostgreSQL 14+ with asyncpg driver |
| **Auth** | JWT (HS256) + Bcrypt |
| **AI / LLM** | Ollama (llama3:latest) — fully local |
| **Deployment** | Vercel (frontend) · Render (backend + DB) |

---

## 🔒 Security Highlights

- JWT tokens with 30-minute expiry and role-based access control (RBAC)
- Bcrypt password hashing (12 rounds)
- SQL injection protection via SQLAlchemy parameterized queries
- CORS restricted to frontend domain only
- Secrets managed via environment variables (never committed)

---

## 💡 Why This Project Stands Out

Most booking system tutorials stop at basic CRUD. This one goes further:

- **AI built on fundamentals** — the recommendation engine uses a transparent, well-reasoned scoring formula instead of a library call. This shows algorithmic thinking, not just tool usage.
- **Real product thinking** — when a booking fails, the system doesn't dead-end. It suggests alternatives, which is what a real product would do.
- **Local LLM integration** — the chatbot uses Ollama for general queries, meaning zero API cost and full data privacy.
- **Clean API design** — all endpoints follow a unified response envelope (`{ data, meta, error }`), making the API predictable and easy to consume.
- **Async all the way** — FastAPI + asyncpg ensures non-blocking database operations under load.
- **Fully deployed** — not a localhost demo. Both frontend and backend are live on real infrastructure.

---

## 🔑 Key Technical Highlights

- **Async FastAPI backend** with SQLAlchemy async ORM and connection pooling
- **Pure SQL recommendation scoring** — no ML framework overhead, fully explainable output
- **Intent-based chatbot routing** — rule-based NLP with LLM fallback for graceful degradation
- **Smart booking suggestions** — automatic alternative date/time generation on conflict
- **Alembic migrations** — versioned schema changes ready for production workflows
- **RBAC with JWT** — customer and admin roles with route-level enforcement
- **Unified API response format** — consistent envelope for all success, list, pagination, and error responses

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+, Node.js 18+, PostgreSQL 14+

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # fill in DATABASE_URL, SECRET_KEY, etc.

# Run migrations and start server
alembic upgrade head
uvicorn app.main:app --reload --port 8000
# API docs → http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env  # set VITE_API_BASE_URL=http://localhost:8000/api/v1
npm run dev
# App → http://localhost:5173
```

### Create Admin Account
1. Register via `/register`
2. Run in PostgreSQL: `UPDATE users SET role = 'admin' WHERE email = 'your@email.com';`

---

## 📁 Project Structure

```
restaurant-booking/
├── backend/
│   └── app/
│       ├── api/v1/endpoints/     # Route handlers
│       ├── services/             # Business logic + AI
│       │   ├── recommendation_service.py
│       │   ├── chatbot_service.py
│       │   └── smart_booking_service.py
│       ├── models/               # SQLAlchemy ORM models
│       ├── schemas/              # Pydantic request/response
│       └── core/                 # Config, JWT, security
└── frontend/
    └── src/
        ├── views/                # Pages (auth, booking, admin)
        ├── components/           # Chatbot widget + UI
        ├── services/             # API calls
        └── stores/               # Pinia global state
```

---

## ☁️ Deployment

| Component | Platform | URL |
|-----------|----------|-----|
| Frontend | Vercel | [restaurant-booking-bice.vercel.app](https://restaurant-booking-bice.vercel.app) |
| Backend API | Render | [restaurant-booking-api-sj8b.onrender.com](https://restaurant-booking-api-sj8b.onrender.com) |
| Database | Render PostgreSQL | Managed cloud instance |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

**Version:** 1.0.0 · **Status:** ✅ Production Ready · **Last Updated:** April 2026