#!/bin/bash
# Chạy migration trước
DATABASE_URL=$ALEMBIC_DATABASE_URL alembic upgrade head || echo "Migration failed, continuing..."
# Khởi động server
uvicorn app.main:app --host 0.0.0.0 --port $PORT
 