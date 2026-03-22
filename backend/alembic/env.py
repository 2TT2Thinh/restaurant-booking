from logging.config import fileConfig
import sys
import os
from os.path import abspath, dirname
from dotenv import load_dotenv

# Load .env file TRƯỚC KHI đọc environment variable
load_dotenv(os.path.join(dirname(dirname(abspath(__file__))), '.env'))

sys.path.insert(0, dirname(dirname(abspath(__file__))))
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config

# Đọc DATABASE_URL từ environment (production) hoặc alembic.ini (local)
database_url = os.environ.get("ALEMBIC_DATABASE_URL") or os.environ.get("DATABASE_URL")
if database_url:
    database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.models.base import Base
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.booking import Booking
target_metadata = Base.metadata