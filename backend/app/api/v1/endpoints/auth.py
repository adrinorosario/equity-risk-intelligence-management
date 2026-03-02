# TLDR; Authentication endpoints (register/login/token refresh).
# TODO: Implement secure registration/login and role-aware token issuance per SRS FR1/FR6.

from fastapi import APIRouter

from app.schemas.user import UserCreate, UserLogin, UserPublic
from app.services.auth_service import AuthService


router = APIRouter()

# NOTE: Intentionally no route implementations yet (structure-only scaffold).
