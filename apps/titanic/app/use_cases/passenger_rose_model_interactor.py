from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schemas import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository


class RoseModelInteractor(RoseModelUseCase):
    def __init__(self, repository: RoseModelRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        query = RoseModelQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
