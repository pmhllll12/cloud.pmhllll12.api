"""Walter 업로드 승객 행 ORM — `Sex` → `gender`."""

from __future__ import annotations

from typing import Any

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class WalterPassenger(Base):
    __tablename__ = "titanic_walter_passengers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    upload_filename: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    passenger_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    survived: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pclass: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(10), nullable=True)
    age: Mapped[float | None] = mapped_column(Float, nullable=True)
    sib_sp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parch: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ticket: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fare: Mapped[float | None] = mapped_column(Float, nullable=True)
    cabin: Mapped[str | None] = mapped_column(String(50), nullable=True)
    embarked: Mapped[str | None] = mapped_column(String(5), nullable=True)

    @classmethod
    def from_record(cls, filename: str, row: dict[str, Any]) -> WalterPassenger:
        return cls(
            upload_filename=filename,
            passenger_id=_as_int(row.get("PassengerId")),
            survived=_as_int(row.get("Survived")),
            pclass=_as_int(row.get("Pclass")),
            name=_as_str(row.get("Name")),
            gender=_as_str(row.get("gender")),
            age=_as_float(row.get("Age")),
            sib_sp=_as_int(row.get("SibSp")),
            parch=_as_int(row.get("Parch")),
            ticket=_as_str(row.get("Ticket")),
            fare=_as_float(row.get("Fare")),
            cabin=_as_str(row.get("Cabin")),
            embarked=_as_str(row.get("Embarked")),
        )

    def to_api_row(self) -> dict[str, Any]:
        return {
            "PassengerId": self.passenger_id,
            "Survived": self.survived,
            "Pclass": self.pclass,
            "Name": self.name,
            "gender": self.gender,
            "Age": self.age,
            "SibSp": self.sib_sp,
            "Parch": self.parch,
            "Ticket": self.ticket,
            "Fare": self.fare,
            "Cabin": self.cabin,
            "Embarked": self.embarked,
        }


def _as_str(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and value != value):
        return None
    text = str(value).strip()
    return text or None


def _as_int(value: Any) -> int | None:
    if value is None or (isinstance(value, float) and value != value):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _as_float(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and value != value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
