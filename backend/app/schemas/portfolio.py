# TLDR; Portfolio schemas for creating and displaying portfolios.
# TODO: Add computed fields (risk level, totals) and ownership constraints.

from datetime import date
from pydantic import BaseModel, Field


class PortfolioBase(BaseModel):
    portfolio_name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=200)


class PortfolioCreate(PortfolioBase):
    user_id: int


class PortfolioUpdate(BaseModel):
    portfolio_name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=200)
    total_value: float | None = Field(default=None, ge=0)
    risk_level: str | None = Field(default=None, max_length=20)


class PortfolioPublic(PortfolioBase):
    portfolio_id: int
    user_id: int
    creation_date: date | None = None
    total_value: float | None = None
    risk_level: str | None = None
