# TLDR; PostgreSQL async SQLAlchemy engine/session wiring.
# TODO: Add pool tuning, health checks, and transactional patterns per service.

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.core.config import get_settings

SQL_ALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"


def get_postgres_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(settings.postgres_dsn, pool_pre_ping=True)


async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    engine = get_postgres_engine()
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
