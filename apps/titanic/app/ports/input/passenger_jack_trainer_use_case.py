from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schemas import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse


class JackTrainerUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        """잭(트레이너) 자기소개."""
        raise NotImplementedError
