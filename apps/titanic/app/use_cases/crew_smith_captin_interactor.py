from __future__ import annotations

import logging

from fastapi import Depends

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema, SmithCaptainSchema, SmithCaptainChatSchema
from tailor.apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse, ChatResponse
from tailor.apps.titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from tailor.apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from tailor.apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from tailor.apps.titanic.app.ports.input.passenger_cal_tester_use_case import caltesterUseCase
from tailor.apps.titanic.app.ports.input.crew_walter_roaster_use_case import walterroasterUseCase
from tailor.apps.titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from tailor.apps.titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor
from tailor.apps.titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor
from tailor.apps.titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case
from tailor.apps.titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case

logger = logging.getLogger(__name__)

class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository):
        self.jack: JackTrainerUseCase,
        self.rose: RoseModelUseCase,
        self.cal: CalTesterUseCase,
        self.walter: WalterRoasterUseCase


    async def chat(self, schema: ChatSchema) -> ChatResponse:
        logger.info(f"[SmithCaptainInteractor] chat 진입 | messages={schema.messages}")
        train_set = self.walter.get_train_set()
        test_set = self.walter.get_test_set()
        self.jack.train_model(train_set)
        self.cal.test_model(test_set)

        return "1309명 입니다"


    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(SmithCaptainQuery(
            id = schema.id,
            name = schema.name
        ))

 