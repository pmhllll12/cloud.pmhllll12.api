import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository

logger = logging.getLogger(__name__)


class WalterRoasterPgRepository(WalterRoasterRepository):
    """PostgreSQL 월터의 승객 명단 관리 저장소 (스텁)."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self.session = session

    def introduce_myself(self, query: WalterRoasterQuery) -> None:
        """승객 명단을 가져오는 메소드 — DB 연동 전 로그만."""
        logger.info("########################################################")
        logger.info("[월터 PG 저장소] DTO 수신")
        logger.info("ID: %s", query.id)
        logger.info("이름: %s", query.name)
        logger.info("메모: %s", query.memo)
        logger.info("########################################################")
