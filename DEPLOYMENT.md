# 🚀 Deployment Guide - Restaurant Booking System

## ✅ Pre-Deployment Checklist

### 1. Environment & Secrets
```bash
# ✅ Verify .env is in .gitignore (NOT git committed)
grep ".env" .gitignore

# ✅ Generate new SECRET_KEY
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"

# ✅ Create .env from template
cp backend/.env.example backend/.env

# ✅ Edit backend/.env with production values:
ENVIRONMENT=production
SECRET_KEY=<new_random_value>
DATABASE_URL=postgresql+asyncpg://user:STRONG_PASSWORD@host:5432/db
FRONTEND_URL=https://yourdomain.com
OLLAMA_HOST=<production_ollama_or_api_endpoint>
SENTRY_DSN=<optional_error_tracking>
```

### 2. Database Setup
```bash
# ✅ Verify PostgreSQL is running and accessible
psql -h YOUR_HOST -U booking_user -d restaurant_booking -c "SELECT 1"

# ✅ Run migrations
cd backend
DATABASE_URL="postgresql://..." alembic upgrade head
```

### 3. Security Verification
```bash
# ✅ Verify no hardcoded credentials in code
grep -r "123456" backend/app/  # Should find NOTHING
grep -r "secret" backend/app/  # Only in comments/config

# ✅ Verify .env NOT committed
git log -p backend/.env | head  # Should show nothing

# ✅ CORS whitelist updated for production domain
# Edit backend/app/core/config.py ENVIRONMENT=production
```

---

## 🎯 Deploy on Render.com (Recommended for Demo)

### Step 1: Prepare GitHub
```bash
# Make sure everything is committed
git add .
git commit -m "feat: prepare for production deployment"
git push origin main

# ✅ Verify .env is NOT in git
git ls-files | grep -E "\.env$"  # Should be empty
```

### Step 2: Create Render Service

1. Go to [render.com](https://render.com)
2. Click **New +** → **Web Service**
3. Connect GitHub repo
4. Configure:
   - **Name:** `restaurant-booking-api`
   - **Root Directory:** `backend/`
   - **Runtime:** Python 3.11
   - **Build Command:** `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command:** 
     ```
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

### Step 3: Set Environment Variables

In Render dashboard → **Environment**:
```
ENVIRONMENT=production
SECRET_KEY=<generated_secret>
DATABASE_URL=postgresql+asyncpg://...
FRONTEND_URL=https://yourdomain.com
OLLAMA_HOST=http://ollama-service:11434
INTERNAL_BASE_URL=https://api.yourdomain.com/api/v1
```

### Step 4: Deploy
- Click **Deploy**
- Wait for build (~3-5 min)
- Verify health check: `https://api.yourdomain.com/health`

---

## 🐳 Deploy with Docker (Advanced)

### Create Dockerfile
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

# Run migrations + start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

### Build & Push
```bash
docker build -t restaurant-booking:latest backend/
docker tag restaurant-booking:latest your-registry/restaurant-booking:latest
docker push your-registry/restaurant-booking:latest
```

### Deploy on Heroku (if using Docker)
```bash
heroku login
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name
```

---

## ✅ Post-Deployment Verification

### 1. Health Check Endpoints
```bash
# API health
curl https://api.yourdomain.com/health

# Chatbot health
curl -H "Authorization: Bearer <test_token>" \
  https://api.yourdomain.com/api/v1/chat/health
```

### 2. Test Core Flows
```bash
# 1. Register user
curl -X POST https://api.yourdomain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Password123","full_name":"Test"}'

# 2. Login
curl -X POST https://api.yourdomain.com/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=Password123"

# 3. Get token from response, then test recommend
curl -H "Authorization: Bearer <token>" \
  https://api.yourdomain.com/api/v1/recommendations/restaurants

# 4. Test chatbot
curl -X POST https://api.yourdomain.com/api/v1/chat/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"gợi ý nhà hàng"}]}'
```

### 3. Monitor Logs
```bash
# Render: Dashboard → Logs
# Heroku: heroku logs --tail
# Check for errors, especially JWT/Auth failures
```

---

## 🔒 Security Best Practices

### Rotate Secrets Regularly
```bash
# Generate new SECRET_KEY every 6 months
python -c "import secrets; print(secrets.token_hex(32))"
# Update in environment variables
```

### Enable HTTPS Everywhere
- ✅ Render/Heroku auto-enable HTTPS
- ✅ Redirect HTTP → HTTPS (usually auto)

### Monitor & Log
- Set up Sentry for error tracking
- Enable structured JSON logging
- Monitor failed login attempts

### Database Backup
```bash
# Render: Automatic daily backups
# Manual backup:
pg_dump -h YOUR_HOST -U booking_user restaurant_booking > backup.sql
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| `401 Unauthorized` on /chat | Token expired or invalid, re-login |
| `getaddrinfo failed` | INTERNAL_BASE_URL misconfigured for environment |
| Database connection error | Verify DATABASE_URL credentials + network access |
| `Secret key too short` | Generate 32+ char SECRET_KEY |
| CORS error | Update ALLOWED_ORIGINS for new domain |
| Ollama not found | Set OLLAMA_HOST correctly for deployment env |

---

## 📊 Monitoring Dashboard (Optional)

### Sentry Integration
1. Create [sentry.io](https://sentry.io) project
2. Add to `backend/.env`:
   ```
   SENTRY_DSN=https://key@sentry.io/project-id
   ```
3. Backend auto-reports errors

### Database Monitoring
- Cloud provider dashboard (Render/AWS)
- Monitor connection pool usage
- Track query performance

---

## 🎉 Deployment Complete!

Your API is now live at: `https://api.yourdomain.com`

**Next Steps:**
1. ✅ Deploy frontend to hosting (Vercel/Netlify)
2. ✅ Set frontend's VITE_API_BASE_URL to production API
3. ✅ Test full end-to-end flow
4. ✅ Enable monitoring & logging
5. ✅ Plan disaster recovery

