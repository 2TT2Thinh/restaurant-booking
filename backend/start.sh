#!/bin/bash
echo "==> Running database migrations..."

if [ -n "$ALEMBIC_DATABASE_URL" ]; then
    echo "ALEMBIC_DATABASE_URL found: $ALEMBIC_DATABASE_URL"
    DATABASE_URL=$ALEMBIC_DATABASE_URL alembic upgrade head --verbose
else
    echo "No ALEMBIC_DATABASE_URL, using DATABASE_URL"
    SYNC_URL=$(echo $DATABASE_URL | sed 's/postgresql+asyncpg/postgresql/g')
    echo "SYNC_URL: $SYNC_URL"
    DATABASE_URL=$SYNC_URL alembic upgrade head --verbose
fi

echo "==> Starting server..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT