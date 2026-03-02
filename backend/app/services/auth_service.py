# TLDR; Auth use cases (register/login/role checks) — scaffold only.
# TODO: Implement password hashing, user lookup, JWT issuance, and role enforcement.

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotImplementedFeatureError
from app.schemas.user import UserCreate, UserLogin, UserPublic


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, payload: UserCreate) -> UserPublic:
        raise NotImplementedFeatureError("register not implemented")

    async def login(self, payload: UserLogin) -> str:
        raise NotImplementedFeatureError("login not implemented")
