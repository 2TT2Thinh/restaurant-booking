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

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    ALLOWED_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    # Environment
    ENVIRONMENT: str = "development"

    # External APIs — all optional until feature is enabled
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY:   Optional[str] = None   # Required for chatbot feature

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def model_post_init(self, __context) -> None:
        if not self.ALLOWED_ORIGINS or self.ALLOWED_ORIGINS == ["http://localhost:5173"]:
            self.ALLOWED_ORIGINS = [self.FRONTEND_URL]


settings = Settings()