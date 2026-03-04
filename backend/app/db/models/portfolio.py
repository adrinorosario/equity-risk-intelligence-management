from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Portfolio(Base):
    __tablename__ = "portfolio"
    __table_args__ = (
        CheckConstraint("total_value >= 0", name="total_value_non_negative"),
    )

    portfolio_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False, index=True)
    portfolio_name: Mapped[str] = mapped_column(String(100), nullable=False)
    creation_date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    total_value: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)

    user: Mapped["User"] = relationship(back_populates="portfolios")
    equities: Mapped[list["Equity"]] = relationship(back_populates="portfolio", cascade="all, delete-orphan")

