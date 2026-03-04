# TLDR; Security primitives (password hashing + JWT helpers) — scaffold only.
# TODO: Implement token creation/verification and password hashing per NFR1.

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    subject: str, *, expires_minutes: int | None = None, extra: dict[str, Any] | None = None
) -> str:
    settings = get_settings()
    if expires_minutes is None:
        expires_minutes = settings.access_token_expires_minutes

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)

    to_encode: dict[str, Any] = {"sub": subject, "exp": expire}
    if extra:
        to_encode.update(extra)

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt
