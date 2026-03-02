# TLDR; Declarative SQLAlchemy base for ORM models.
# TODO: Add naming conventions and metadata options for consistent migrations.

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
