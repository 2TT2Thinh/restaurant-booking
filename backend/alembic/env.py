from logging.config import fileConfig
import sys
import os
from alembic import context
from sqlalchemy import engine_from_config, pool

# ========== CẤU HÌNH ĐƠN GIẢN CHO PRODUCTION ==========
# Thêm backend vào sys.path - Dùng relative path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import models
from app.models.base import Base
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.booking import Booking

# Alembic config
config = context.config

# ========== QUAN TRỌNG: Lấy DATABASE_URL từ ENV ==========
# Render sẽ set environment variable trực tiếp, không cần .env
database_url = os.environ.get("DATABASE_URL")

if database_url:
    # Chuyển asyncpg -> sync driver cho Alembic
    database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    config.set_main_option("sqlalchemy.url", database_url)

# Logging config (nếu có file)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (sync for Alembic)."""
    # Alembic hoạt động tốt nhất với sync engine
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()