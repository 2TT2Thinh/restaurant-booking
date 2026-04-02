# app/core/config.py
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
import logging


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL database URL")
    
    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL URL")
        return v

    # JWT
    SECRET_KEY: str = Field(..., min_length=32, description="JWT secret key (min 32 chars)")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # Thêm refresh token

    # CORS
    FRONTEND_URL: str = Field(default="http://localhost:5173", description="Frontend URL for CORS")
    ALLOWED_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:5173"],
        description="Comma-separated origins allowed for CORS"
    )
    CORS_ALLOW_CREDENTIALS: bool = True

    # Environment
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production|testing)$")
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"

    # External APIs - Ollama
    OLLAMA_MODEL_NAME: str = "llama3:latest"  # Sửa từ llama3.2:latest thành llama3:latest
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_TIMEOUT: int = Field(default=120, ge=10, le=300, description="Ollama timeout in seconds")
    OLLAMA_KEEP_ALIVE: int = Field(default=300, description="Keep model loaded for N seconds")
    
    @field_validator("OLLAMA_HOST")
    def validate_ollama_host(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("OLLAMA_HOST must start with http:// or https://")
        return v.rstrip("/")

    # Internal API
    INTERNAL_BASE_URL: str = Field(
        default="http://localhost:8000/api/v1",
        description="Internal API URL for service-to-service communication"
    )
    INTERNAL_API_TIMEOUT: int = Field(default=30, ge=5, le=60)
    
    @field_validator("INTERNAL_BASE_URL")
    def validate_internal_url(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("INTERNAL_BASE_URL must start with http:// or https://")
        return v.rstrip("/")

    # Google Maps
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    LOG_FORMAT: str = "json"  # json or text
    
    # Rate Limiting (optional Redis)
    REDIS_URL: Optional[str] = None
    RATE_LIMIT_REQUESTS: int = Field(default=100, ge=1, le=1000)
    RATE_LIMIT_PERIOD: int = Field(default=60, ge=1, le=3600)
    
    # Security
    PASSWORD_MIN_LENGTH: int = Field(default=8, ge=6, le=128)
    PASSWORD_REQUIRE_DIGIT: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True
    BCRYPT_ROUNDS: int = Field(default=12, ge=8, le=15)
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    ENABLE_METRICS: bool = False
    METRICS_PORT: int = Field(default=9090, ge=1024, le=65535)
    
    # Performance
    DB_POOL_SIZE: int = Field(default=20, ge=5, le=100)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0, le=50)
    DB_POOL_TIMEOUT: int = Field(default=30, ge=1, le=120)
    
    # Feature flags
    ENABLE_CHATBOT_CACHE: bool = False
    CHATBOT_CACHE_TTL: int = Field(default=3600, ge=60, le=86400)  # seconds

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra env vars
        case_sensitive=False,
    )

    def model_post_init(self, __context) -> None:
        """Post-initialization processing"""
        # Only override ALLOWED_ORIGINS if it's still the default value
        if self.ALLOWED_ORIGINS == ["http://localhost:5173"]:
            self.ALLOWED_ORIGINS = [self.FRONTEND_URL]
        
        # Validate production requirements
        if self.is_production:
            self._validate_production_config()
    
    def _validate_production_config(self) -> None:
        """Validate critical settings for production"""
        if len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters in production")
        
        if not self.INTERNAL_BASE_URL.startswith("https://"):
            # Allow HTTP only in development
            if self.is_production:
                raise ValueError("INTERNAL_BASE_URL must use HTTPS in production")
        
        if self.ENVIRONMENT == "production" and not self.SENTRY_DSN:
            # Warning, not error
            logging.warning("SENTRY_DSN not configured in production")


settings = Settings()