from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schemas import HartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_repository import HartleyViolinRepository


class HartleyViolinInteractor(HartleyViolinUseCase):
    def __init__(self, repository: HartleyViolinRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        query = HartleyViolinQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
