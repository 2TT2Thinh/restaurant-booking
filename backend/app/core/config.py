# app/core/config.py
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS — comma-separated in .env: ALLOWED_ORIGINS=http://localhost:5173,https://yourapp.com
    FRONTEND_URL: str = "http://localhost:5173"
    ALLOWED_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    # Environment
    ENVIRONMENT: str = "development"

    # Google Maps — optional until feature is implemented
    GOOGLE_MAPS_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def model_post_init(self, __context) -> None:
        """
        If ALLOWED_ORIGINS is not explicitly set in .env,
        fall back to FRONTEND_URL so a single env var is enough.
        """
        if not self.ALLOWED_ORIGINS or self.ALLOWED_ORIGINS == ["http://localhost:5173"]:
            self.ALLOWED_ORIGINS = [self.FRONTEND_URL]


settings = Settings()