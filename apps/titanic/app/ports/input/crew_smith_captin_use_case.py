from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_smith_captin_schemas import SmithCaptainSchema, ChatSchema
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schemas import JackTrainerSchema
from titanic.adapter.inbound.api.schemas.passenger_rose_model_schemas import RoseModelSchema
from titanic.app.dtos.crew_smith_captin_dto import SmithCaptainResponse
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse


class SmithCaptainUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        """스미스 선장의 자기소개 메소드"""
        pass

    @abstractmethod
    async def chat(self, schema: ChatSchema, 
                    jack: JackTrainerUseCase,
                    rose: RoseModelUseCase,
                    ) -> SmithCaptainResponse:
        """사용자 자연어 입력을 받아 채팅 응답을 반환"""
        pass
