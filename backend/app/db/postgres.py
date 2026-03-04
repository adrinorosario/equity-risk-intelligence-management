# TLDR; PostgreSQL async SQLAlchemy engine/session wiring.
# TODO: Add pool tuning, health checks, and transactional patterns per service.

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings


def get_postgres_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(settings.postgres_dsn, pool_pre_ping=True, future=True)


_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an AsyncSession backed by a shared engine."""
    global _engine, _session_factory

    if _engine is None:
        _engine = get_postgres_engine()

    if _session_factory is None:
        _session_factory = async_sessionmaker(
            _engine,
            expire_on_commit=False,
            autoflush=False,
        )

    async with _session_factory() as session:
        yield session
