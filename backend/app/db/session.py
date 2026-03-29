# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# Convert standard postgresql:// URL to asyncpg driver URL
_db_url = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
).replace(
    "postgres://", "postgresql+asyncpg://"  # Render uses postgres:// scheme
)

engine = create_async_engine(
    _db_url,
    # Only log SQL in development — never in production (floods logs, leaks query structure)
    echo=settings.ENVIRONMENT == "development",
    future=True,
    # Connection pool tuning for production
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Detect stale connections before use
)

# Use async_sessionmaker (preferred over sessionmaker in SQLAlchemy 2.0)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)