#!/bin/bash
echo "==> Running database migrations..."

if [ -n "$ALEMBIC_DATABASE_URL" ]; then
    echo "ALEMBIC_DATABASE_URL found"
    DATABASE_URL=$ALEMBIC_DATABASE_URL alembic upgrade head
    echo "==> Migration exit code: $?"
else
    echo "No ALEMBIC_DATABASE_URL found!"
    SYNC_URL=$(echo $DATABASE_URL | sed 's/postgresql+asyncpg/postgresql/g')
    DATABASE_URL=$SYNC_URL alembic upgrade head
    echo "==> Migration exit code: $?"
fi

echo "==> Starting server..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT