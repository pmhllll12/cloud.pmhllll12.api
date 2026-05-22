"""soccer — 축구 관련 데이터베이스 모델 패키지."""

from soccer.models.group import TournamentGroup
from soccer.models.team import Team
from soccer.models.person import Person, Player, Coach, Referee
from soccer.models.match import Match

__all__ = [
    "TournamentGroup",
    "Team",
    "Person",
    "Player",
    "Coach",
    "Referee",
    "Match",
]
