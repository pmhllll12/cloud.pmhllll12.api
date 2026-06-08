"""James ORM — API 스키마 `titanic.adapter.inbound.api.schemas.crew_james_director_schema` 에 대응."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class JamesBooking(Base):
    __tablename__ = "titanic_bookings"

    booking_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    pclass: Mapped[str] = mapped_column(String(8), nullable=False)
    ticket: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    fare: Mapped[str] = mapped_column(String(32), nullable=False, default="0")
    cabin: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    embarked_code: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    port_name: Mapped[str] = mapped_column(String(128), nullable=False, default="")


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


__all__ = ["JamesBooking", "JamesPerson"]
