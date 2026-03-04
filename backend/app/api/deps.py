# TLDR; FastAPI dependency providers (db sessions, current user, permissions).
# TODO: Implement auth dependencies and connect Postgres/Mongo sessions safely.

from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import pwd_context
from app.db.models.user import User
from app.db.postgres import get_postgres_session
from app.schemas.user import UserPublic


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_postgres_session():
        yield session


DbSession = Depends(get_db_session)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = DbSession,
) -> UserPublic:
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        subject: str | None = payload.get("sub")
        if subject is None:
            raise credentials_exception
        user_id = int(subject)
    except (JWTError, ValueError):
        raise credentials_exception

    user = await db.get(User, user_id)
    if user is None or user.status != "Active":
        raise credentials_exception

    return UserPublic.model_validate(user, from_attributes=True)


async def get_current_active_user(current_user: UserPublic = Depends(get_current_user)) -> UserPublic:
    if current_user.status != "Active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
