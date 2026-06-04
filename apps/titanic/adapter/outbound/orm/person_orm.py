"""James `PersonCommand` — Neon/PostgreSQL ORM (`database.Base` 와 동일 메타데이터)."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class JamesPerson(Base):
    """`PersonCommand` 필드와 1:1. `passenger_id` 는 기본 키."""

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
