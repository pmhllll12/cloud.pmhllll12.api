from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schemas import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainRepository


class JackTrainerInteractor(JackTrainerUseCase):
    def __init__(self, repository: JackTrainRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        query = JackTrainerQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
