from __future__ import annotations

import asyncio
import logging

from kiwipiepy import Kiwi

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schemas import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainRepository

logger = logging.getLogger(__name__)


class JackTrainerInteractor(JackTrainerUseCase):
    def __init__(self, repository: JackTrainRepository, kiwi: Kiwi | None = None) -> None:
        self.repository = repository
        self.kiwi = kiwi if kiwi is not None else Kiwi()

    async def analyze_message_intent(self, user_message: str) -> dict:
        # 사용자의 질문(message)을 형태소를 분석하여 키워드와 의도를 파악한다
        results = await asyncio.to_thread(self.kiwi.analyze, user_message)
        if not results:
            return {"keywords": [], "intent": "unknown", "morphemes": []}

        tokens = results[0][0]

        # 명사(NN*) · 동사(VV) · 형용사(VA) → 키워드
        keywords = [
            t.form for t in tokens
            if str(t.tag).startswith(("NN", "VV", "VA"))
        ]

        # 의문사 포함 여부로 의도 판단
        _QUESTION_WORDS = {"무엇", "뭐", "어디", "어떻게", "왜", "언제", "누구", "몇", "얼마"}
        forms = {t.form for t in tokens}
        intent = "question" if forms & _QUESTION_WORDS else "statement"

        logger.info(
            "[JackTrainerInteractor/analyze] message=%r keywords=%s intent=%s",
            user_message, keywords, intent,
        )

        return {
            "keywords": keywords,
            "intent": intent,
            "morphemes": [{"form": t.form, "tag": str(t.tag)} for t in tokens],
        }

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        query = JackTrainerQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
