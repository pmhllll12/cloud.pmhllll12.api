from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_smith_captin_schemas import SmithCaptainSchema
from titanic.app.dtos.crew_smith_captin_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captin_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captin_repository import SmithCaptainRepository


class SmithCaptainInteractor(SmithCaptainUseCase):
    def __init__(self, repository: SmithCaptainRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        query = SmithCaptainQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
