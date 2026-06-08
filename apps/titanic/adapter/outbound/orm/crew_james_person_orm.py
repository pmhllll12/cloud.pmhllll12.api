"""James Person ORM — `schemas/crew_james_director_schema` 저장 경로."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class JamesPerson(Base):
    __tablename__ = "titanic_persons"

    passenger_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    booking_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    embarked_code: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    gender: Mapped[str] = mapped_column(String(32), nullable=False)
    age: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    sib_sp: Mapped[str] = mapped_column(String(16), nullable=False, default="0")
    parch: Mapped[str] = mapped_column(String(16), nullable=False, default="0")
    survived: Mapped[str] = mapped_column(String(8), nullable=False, default="0")


__all__ = ["JamesPerson"]
