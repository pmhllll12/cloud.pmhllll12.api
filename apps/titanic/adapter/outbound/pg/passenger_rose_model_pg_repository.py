from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

logger = logging.getLogger(__name__)


class RoseModelPgRepository(RoseModelRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        logger.info("[RoseModelPgRepository] introduce_myself | request_data=%s", query)
        return RoseModelResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )
