# Risk metric + assessment schemas aligned with SRS FR4 tables.

from datetime import date
from pydantic import BaseModel, Field


class RiskMetricBase(BaseModel):
    metric_name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=200)
    threshold_value: float | None = None
    category: str | None = Field(default=None, max_length=50)


class RiskMetricPublic(RiskMetricBase):
    metric_id: int


class RiskAssessmentCreate(BaseModel):
    equity_id: int
    metric_id: int
    analyst_id: int
    risk_score: float = Field(ge=0, le=100)
    assessment_date: date | None = None
    remarks: str | None = Field(default=None, max_length=200)


class RiskAssessmentPublic(RiskAssessmentCreate):
    assessment_id: int
