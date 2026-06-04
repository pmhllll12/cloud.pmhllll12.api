"""James `BookingCommand` — Neon/PostgreSQL ORM (`database.Base` 와 동일 메타데이터)."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class JamesBooking(Base):
    """`BookingCommand` 필드와 1:1. `booking_id` 는 기본 키 (업로드 시 `passenger_id` 와 동일 값 사용)."""

    __tablename__ = "titanic_bookings"

    booking_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    pclass: Mapped[str] = mapped_column(String(8), nullable=False)
    ticket: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    fare: Mapped[str] = mapped_column(String(32), nullable=False, default="0")
    cabin: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    embarked_code: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    port_name: Mapped[str] = mapped_column(String(128), nullable=False, default="")


__all__ = ["JamesBooking"]
