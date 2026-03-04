# TLDR; Equity schemas for storing equities within portfolios.
# TODO: Add symbol/ticker, pricing history references, and exchange validation.

from datetime import date
from pydantic import BaseModel, Field


class EquityBase(BaseModel):
    company_name: str = Field(min_length=1, max_length=150)
    sector: str | None = Field(default=None, max_length=100)
    exchange: str | None = Field(default=None, max_length=50)


class EquityCreate(EquityBase):
    portfolio_id: int
    market_value: float = Field(ge=0)
    purchase_date: date | None = None


class EquityUpdate(BaseModel):
    company_name: str | None = Field(default=None, min_length=1, max_length=150)
    sector: str | None = Field(default=None, max_length=100)
    market_value: float | None = Field(default=None, ge=0)
    exchange: str | None = Field(default=None, max_length=50)


class EquityPublic(EquityBase):
    equity_id: int
    portfolio_id: int
    market_value: float | None = None
    purchase_date: date | None = None
