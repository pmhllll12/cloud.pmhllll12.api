from __future__ import annotations

from datetime import date
from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Person(Base):
    __tablename__ = "soccer_persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(64), nullable=True)
    person_type: Mapped[str] = mapped_column(String(32), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": "person_type",
        "polymorphic_identity": "person",
    }


class Player(Person):
    __tablename__ = "soccer_players"

    id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("soccer_persons.id", ondelete="CASCADE"),
        primary_key=True,
    )
    position: Mapped[str] = mapped_column(String(32), nullable=False)
    jersey_number: Mapped[int] = mapped_column(Integer, nullable=False)
    team_id: Mapped[int | None] = mapped_column(
        ForeignKey("soccer_teams.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    team: Mapped[Team | None] = relationship("Team", back_populates="players")

    __mapper_args__ = {
        "polymorphic_identity": "player",
    }


class Coach(Person):
    __tablename__ = "soccer_coaches"

    id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("soccer_persons.id", ondelete="CASCADE"),
        primary_key=True,
    )
    license_level: Mapped[str] = mapped_column(String(32), nullable=False)
    team_id: Mapped[int | None] = mapped_column(
        ForeignKey("soccer_teams.id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )

    # Relationships
    team: Mapped[Team | None] = relationship("Team", back_populates="coach")

    __mapper_args__ = {
        "polymorphic_identity": "coach",
    }


class Referee(Person):
    __tablename__ = "soccer_referees"

    id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("soccer_persons.id", ondelete="CASCADE"),
        primary_key=True,
    )
    badge_year: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    matches: Mapped[list[Match]] = relationship("Match", back_populates="referee")

    __mapper_args__ = {
        "polymorphic_identity": "referee",
    }
