from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_port import LoweBoatPort


class LoweBoatInteractor(LoweBoatUseCase):
    def __init__(self, repository: LoweBoatPort) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        query = LoweBoatQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
