from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]
    # CORS & Environment
    FRONTEND_URL: str
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

# QUAN TRỌNG: Phải có dòng này để khởi tạo biến settings
settings = Settings()