from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Equity(Base):
    __tablename__ = "equity"
    __table_args__ = (
        CheckConstraint("market_value >= 0", name="market_value_non_negative"),
    )

    equity_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.portfolio_id"), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(150), nullable=False)
    sector: Mapped[str | None] = mapped_column(String(100), nullable=True)
    market_value: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    exchange: Mapped[str | None] = mapped_column(String(50), nullable=True)
    purchase_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    portfolio: Mapped["Portfolio"] = relationship(back_populates="equities")
    risk_assessments: Mapped[list["RiskAssessment"]] = relationship(
        back_populates="equity",
        cascade="all, delete-orphan",
    )

