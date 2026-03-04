# TLDR; User management endpoints (profiles, roles, admin actions).
# TODO: Implement CRUD + role management per SRS FR1/FR6.

from fastapi import APIRouter, Depends

from app.api.deps import get_current_active_user
from app.schemas.user import UserPublic, UserUpdate


router = APIRouter()


@router.get("/me", response_model=UserPublic)
async def read_current_user(current_user: UserPublic = Depends(get_current_active_user)) -> UserPublic:
    return current_user


@router.put("/me", response_model=UserPublic)
async def update_current_user(
    payload: UserUpdate,
    current_user: UserPublic = Depends(get_current_active_user),
) -> UserPublic:
    # For now, simply echo the requested changes on top of the current user representation.
    # A fuller implementation would persist changes via a dedicated UserService.
    updated_data = current_user.model_dump()
    for field, value in payload.model_dump(exclude_unset=True).items():
        updated_data[field] = value
    return UserPublic(**updated_data)
