from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class RiskMetric(Base):
    __tablename__ = "risk_metric"

    metric_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    threshold_value: Mapped[float | None] = mapped_column(Numeric(6, 2), nullable=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="Active")

    assessments: Mapped[list["RiskAssessment"]] = relationship(back_populates="metric")


class RiskAssessment(Base):
    __tablename__ = "risk_assessment"
    __table_args__ = (
        CheckConstraint("risk_score >= 0 AND risk_score <= 100", name="risk_score_between_0_100"),
    )

    assessment_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    equity_id: Mapped[int] = mapped_column(ForeignKey("equity.equity_id"), nullable=False, index=True)
    metric_id: Mapped[int] = mapped_column(ForeignKey("risk_metric.metric_id"), nullable=False, index=True)
    analyst_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False, index=True)
    risk_score: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)
    assessment_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    remarks: Mapped[str | None] = mapped_column(String(200), nullable=True)

    equity: Mapped["Equity"] = relationship(back_populates="risk_assessments")
    metric: Mapped["RiskMetric"] = relationship(back_populates="assessments")
    analyst: Mapped["User"] = relationship(back_populates="assessments")

