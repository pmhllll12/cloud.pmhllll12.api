from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schemas import AndrewsArchitectSchema
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository


class AndrewsArchitectInteractor(AndrewsArchitectUseCase):
    def __init__(self, repository: AndrewsArchitectRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        query = AndrewsArchitectQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
