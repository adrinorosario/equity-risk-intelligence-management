from datetime import date

from sqlalchemy import Date, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False, server_default="Investor")
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="Active")

    portfolios: Mapped[list["Portfolio"]] = relationship(back_populates="user")
    assessments: Mapped[list["RiskAssessment"]] = relationship(back_populates="analyst")

