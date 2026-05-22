from __future__ import annotations

from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Match(Base):
    __tablename__ = "soccer_matches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kickoff_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    round: Mapped[str] = mapped_column(String(64), nullable=False)
    venue: Mapped[str] = mapped_column(String(100), nullable=False)
    
    home_team_id: Mapped[int] = mapped_column(
        ForeignKey("soccer_teams.id", ondelete="CASCADE"),
        nullable=False,
    )
    away_team_id: Mapped[int] = mapped_column(
        ForeignKey("soccer_teams.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    referee_id: Mapped[int | None] = mapped_column(
        ForeignKey("soccer_referees.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    home_team: Mapped[Team] = relationship(
        "Team",
        foreign_keys=[home_team_id],
        back_populates="home_matches",
    )
    
    away_team: Mapped[Team] = relationship(
        "Team",
        foreign_keys=[away_team_id],
        back_populates="away_matches",
    )
    
    referee: Mapped[Referee | None] = relationship("Referee", back_populates="matches")
