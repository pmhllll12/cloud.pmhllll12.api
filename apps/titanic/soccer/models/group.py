from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from soccer.models.team import Team


class TournamentGroup(Base):
    """월드컵 본선 A조·B조 등 대회 단위 조별 구분."""

    __tablename__ = "soccer_tournament_groups"
    __table_args__ = (
        UniqueConstraint(
            "tournament_name",
            "stage",
            "name",
            name="uq_soccer_tournament_group_slot",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tournament_name: Mapped[str] = mapped_column(String(128), nullable=False)
    stage: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    teams: Mapped[list["Team"]] = relationship(
        "Team",
        back_populates="group",
        cascade="all, delete-orphan",
    )
