#!/bin/bash
# Chạy migration trước
alembic upgrade head
# Khởi động server
uvicorn app.main:app --host 0.0.0.0 --port $PORT
 