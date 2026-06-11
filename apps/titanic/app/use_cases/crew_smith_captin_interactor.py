from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_smith_captin_schemas import SmithCaptainSchema
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schemas import JackTrainerSchema
from titanic.adapter.inbound.api.schemas.passenger_rose_model_schemas import RoseModelSchema
from titanic.app.dtos.crew_smith_captin_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse
from titanic.app.ports.input.crew_smith_captin_use_case import SmithCaptainUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captin_repository import SmithCaptainRepository
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer
from titanic.dependencies.passenger_rose_model_provider import get_rose_model

class SmithCaptainInteractor(SmithCaptainUseCase):
    """선장 유스케이스 — 잭·로즈 승객 유스케이스와 조합해 호출할 수 있게 연결합니다."""

    def __init__(
        self,
        repository: SmithCaptainRepository,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
    ) -> None:
        self.repository = repository
        

    async def chat(self, schema: ChatSchema,
    jack: JackTrainerUseCase = Depends(get_jack_trainer),
    rose: RoseModelUseCase = Depends(get_rose_model),
        )-> SmithCaptainResponse:
   

        return await self.repository.chat(schema.message)

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(SmithCaptainQuery(
            id=schema.id, 
            name=schema.name))
