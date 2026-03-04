# TLDR; User/role schemas for auth and profile management.
# TODO: Add password policies, role constraints, and admin-only fields.

from datetime import date
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    role: str = Field(default="Investor", max_length=20)
    status: str = Field(default="Active", max_length=20)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    role: str | None = Field(default=None, max_length=20)
    status: str | None = Field(default=None, max_length=20)


class UserPublic(UserBase):
    user_id: int
    created_at: date | None = None
