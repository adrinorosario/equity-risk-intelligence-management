# PostgreSQL async SQLAlchemy engine/session wiring.
# Falls back to SQLite when Postgres is unavailable.

import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None
_USE_SQLITE = False


def _sqlite_dsn() -> str:
    return "sqlite+aiosqlite:///./erims_dev.db"


async def _try_init_engine() -> AsyncEngine:
    """Try Postgres first, fall back to SQLite."""
    global _USE_SQLITE
    settings = get_settings()

    try:
        engine = create_async_engine(settings.postgres_dsn, pool_pre_ping=True, future=True)
        # Test the actual connection
        async with engine.connect() as conn:
            await conn.execute(
                __import__("sqlalchemy").text("SELECT 1")
            )
        logger.info("Connected to PostgreSQL")
        return engine
    except Exception as exc:
        logger.warning("PostgreSQL unavailable (%s), falling back to SQLite", exc)
        _USE_SQLITE = True
        return create_async_engine(_sqlite_dsn(), future=True)


def get_postgres_engine() -> AsyncEngine:
    """Synchronous engine getter — only used by lifespan which awaits init."""
    settings = get_settings()
    return create_async_engine(settings.postgres_dsn, pool_pre_ping=True, future=True)


async def init_engine() -> AsyncEngine:
    """Async engine initialisation with Postgres/SQLite fallback."""
    global _engine, _session_factory
    _engine = await _try_init_engine()
    _session_factory = async_sessionmaker(_engine, expire_on_commit=False, autoflush=False)
    return _engine


async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an AsyncSession backed by a shared engine."""
    global _engine, _session_factory

    if _engine is None:
        await init_engine()

    async with _session_factory() as session:
        yield session
