from logging.config import fileConfig
import sys
import os
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config

# ĐỌC DATABASE_URL TỪ ENVIRONMENT VARIABLE (production)
# Nếu không có thì dùng từ alembic.ini (local)
database_url = os.environ.get("ALEMBIC_DATABASE_URL") or os.environ.get("DATABASE_URL")
if database_url:
    # Đảm bảo dùng psycopg2 (sync) cho alembic, không dùng asyncpg
    database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.models.base import Base
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.booking import Booking
target_metadata = Base.metadata