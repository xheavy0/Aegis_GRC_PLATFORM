from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List

_INSECURE_SECRET = "change-this-secret-key"


class Settings(BaseSettings):
    APP_NAME: str = "Aegis GRC Platform"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = False

    DATABASE_URL: str = "postgresql://aegis:aegis_pass@localhost:5432/aegis_grc"

    SECRET_KEY: str = _INSECURE_SECRET
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost:5500"]

    FIRST_ADMIN_EMAIL: str = "admin@aegis.local"
    FIRST_ADMIN_PASSWORD: str = "Admin@1234"
    FIRST_ADMIN_NAME: str = "Administrator"

    @field_validator("SECRET_KEY")
    @classmethod
    def secret_key_must_be_set(cls, v: str, info) -> str:
        import os
        if os.getenv("APP_ENV", "development") == "production" and v == _INSECURE_SECRET:
            raise ValueError(
                "SECRET_KEY must be set to a strong random value in production. "
                "Generate one with: openssl rand -hex 32"
            )
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
