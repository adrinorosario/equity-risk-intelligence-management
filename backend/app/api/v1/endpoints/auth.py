# TLDR; Authentication endpoints (register/login/token refresh).
# TODO: Implement secure registration/login and role-aware token issuance per SRS FR1/FR6.

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import DbSession
from app.schemas.user import UserCreate, UserLogin, UserPublic
from app.services.auth_service import AuthService


router = APIRouter()


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate, db=DbSession) -> UserPublic:
    service = AuthService(db)
    try:
        return await service.register(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login")
async def login(payload: UserLogin, db=DbSession) -> dict[str, str]:
    service = AuthService(db)
    try:
        token = await service.login(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return {"access_token": token, "token_type": "bearer"}
