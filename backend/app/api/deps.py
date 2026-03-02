# TLDR; FastAPI dependency providers (db sessions, current user, permissions).
# TODO: Implement auth dependencies and connect Postgres/Mongo sessions safely.

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import get_postgres_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_postgres_session():
        yield session


DbSession = Depends(get_db_session)
