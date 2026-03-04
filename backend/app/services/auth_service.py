# TLDR; Auth use cases (register/login/role checks) — scaffold only.
# TODO: Implement password hashing, user lookup, JWT issuance, and role enforcement.

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserPublic


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, payload: UserCreate) -> UserPublic:
        existing_user = await self._get_user_by_email(payload.email)
        if existing_user:
            # FastAPI will turn this into a 400/409 via HTTPException in the route layer if desired.
            raise ValueError("User with this email already exists")

        hashed_password = get_password_hash(payload.password)
        user = User(
            name=payload.name,
            email=payload.email,
            role=payload.role,
            password_hash=hashed_password,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return UserPublic.model_validate(user, from_attributes=True)

    async def login(self, payload: UserLogin) -> str:
        user = await self._get_user_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise ValueError("Incorrect email or password")

        token = create_access_token(
            subject=str(user.user_id),
            extra={"role": user.role},
        )
        return token

    async def _get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
