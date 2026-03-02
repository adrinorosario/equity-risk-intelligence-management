# TLDR; User management endpoints (profiles, roles, admin actions).
# TODO: Implement CRUD + role management per SRS FR1/FR6.

from fastapi import APIRouter

from app.schemas.user import UserCreate, UserPublic, UserUpdate
from app.services.auth_service import AuthService


router = APIRouter()

# NOTE: Intentionally no route implementations yet (structure-only scaffold).
