from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository

logger = logging.getLogger(__name__)


class WalterRoasterPgRepository(WalterRoasterRepository):
    """PostgreSQL을 이용한 월터의 승객 명단 관리 저장소 (스텁)."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        logger.info("[WalterRoasterPgRepository] introduce_myself id=%s name=%s", query.id, query.name)
        return WalterRoasterResponse(
            id=query.id,
            name=query.name,
            memo=query.memo,
        )


WalterPgRepository = WalterRoasterPgRepository
