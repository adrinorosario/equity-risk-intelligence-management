# TLDR; Centralized config using environment variables (FastAPI + DB + security).
# TODO: Add per-environment overrides, secrets management, and config validation rules.

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_env: str = "local"
    app_name: str = "erims-api"

    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]

    # Postgres
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "erims"
    postgres_user: str = "erims"
    postgres_password: str = "erims_password"

    # Mongo
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_db: str = "erims"
    mongo_user: str = "erims"
    mongo_password: str = "erims_password"

    # Auth
    jwt_secret: str = "change_me_in_env"
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def mongo_dsn(self) -> str:
        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
