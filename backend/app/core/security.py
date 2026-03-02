# TLDR; Security primitives (password hashing + JWT helpers) — scaffold only.
# TODO: Implement token creation/verification and password hashing per NFR1.

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings
from app.core.exceptions import NotImplementedFeatureError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: str, *, expires_minutes: int | None = None, extra: dict[str, Any] | None = None
) -> str:
    _ = (subject, expires_minutes, extra, get_settings, datetime, timedelta, timezone, jwt)
    raise NotImplementedFeatureError("create_access_token not implemented")
