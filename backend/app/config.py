"""Centralized application configuration.

All configuration is read from environment variables (or a local .env file
in development). Nothing in this codebase should call `os.environ` directly
outside of this module — import `settings` instead, everywhere.

Note: this file defines settings fields for later phases too (Google
Calendar, Twilio, Vapi, etc.) even though nothing uses them yet. Declaring
them now means the .env.example file stays stable as the project grows —
you set the real secrets once, phase by phase, instead of the schema
shifting under you.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- App ---
    PROJECT_NAME: str = "Physiotherapy AI Receptionist"
    ENV: str = "development"  # development | staging | production
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/physio_receptionist"

    # --- Auth (wired up in the Security phase) ---
    JWT_SECRET_KEY: str = "insecure-dev-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]

    # --- AI / RAG (wired up in later phases) ---
    OPENAI_API_KEY: str | None = None
    OPENAI_CHAT_MODEL: str = "gpt-4.1"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHROMA_PERSIST_DIR: str = "./chroma_data"

    # --- Google Calendar (Appointment Management phase) ---
    GOOGLE_CALENDAR_CREDENTIALS_JSON: str | None = None
    GOOGLE_CALENDAR_ID: str | None = None

    # --- Twilio / WhatsApp (WhatsApp phase) ---
    TWILIO_ACCOUNT_SID: str | None = None
    TWILIO_AUTH_TOKEN: str | None = None
    TWILIO_WHATSAPP_NUMBER: str | None = None

    # --- Voice (Voice Receptionist phase) ---
    VAPI_API_KEY: str | None = None
    DEEPGRAM_API_KEY: str | None = None
    ELEVENLABS_API_KEY: str | None = None

    # --- Email (notifications) ---
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_FROM_ADDRESS: str | None = None

    # --- Clinic defaults (used to seed ClinicSettings in Phase 2) ---
    CLINIC_NAME: str = "Physiotherapy Clinic"
    CLINIC_TIMEZONE: str = "Asia/Kolkata"


@lru_cache
def get_settings() -> Settings:
    """Cached settings accessor.

    Using lru_cache means the .env file is parsed once per process, not on
    every import — and tests can call `get_settings.cache_clear()` to
    re-read the environment when needed.
    """
    return Settings()


settings = get_settings()
