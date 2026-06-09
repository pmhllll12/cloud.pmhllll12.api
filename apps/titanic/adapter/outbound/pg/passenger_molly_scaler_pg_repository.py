from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerQuery, MollyScalerResponse
from titanic.app.ports.output.passenger_molly_scaler_repository import MollyScalerRepository

logger = logging.getLogger(__name__)


class MollyScalerPgRepository(MollyScalerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: MollyScalerQuery) -> MollyScalerResponse:
        logger.info("[MollyScalerPgRepository] introduce_myself | request_data=%s", query)
        return MollyScalerResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )
