# Reporting schemas for risk evaluations and exports.

from datetime import date
from typing import Any
from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    portfolio_id: int
    created_by_user_id: int
    report_type: str = Field(default="risk_summary", max_length=50)


class ReportPublic(ReportCreate):
    report_id: int
    created_at: date | None = None
    summary: dict[str, Any] | None = None
