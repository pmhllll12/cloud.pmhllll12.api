from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from soccer.models.group import TournamentGroup


class Team(Base):
    __tablename__ = "soccer_teams"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False, index=True)
    group_id: Mapped[int | None] = mapped_column(
        ForeignKey("soccer_tournament_groups.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    group: Mapped[TournamentGroup | None] = relationship(
        "TournamentGroup",
        back_populates="teams",
    )
    
    players: Mapped[list[Player]] = relationship(
        "Player",
        back_populates="team",
        cascade="all, delete-orphan",
    )
    
    coach: Mapped[Coach | None] = relationship(
        "Coach",
        back_populates="team",
        uselist=False,
    )

    home_matches: Mapped[list[Match]] = relationship(
        "Match",
        foreign_keys="[Match.home_team_id]",
        back_populates="home_team",
    )
    
    away_matches: Mapped[list[Match]] = relationship(
        "Match",
        foreign_keys="[Match.away_team_id]",
        back_populates="away_team",
    )
