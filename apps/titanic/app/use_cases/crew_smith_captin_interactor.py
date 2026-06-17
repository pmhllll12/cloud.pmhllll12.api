from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.crew_smith_captin_schemas import SmithCaptainSchema, SmithChatRequest, SmithChatResponse
from titanic.app.dtos.crew_smith_captin_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.input.crew_smith_captin_use_case import SmithCaptainUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captin_port import SmithCaptainPort

logger = logging.getLogger(__name__)


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(
        self,
        repository: SmithCaptainPort,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
        cal: CalTesterUseCase,
        walter: WalterRoasterUseCase,
        andrews: AndrewsArchitectUseCase,
    ) -> None:
        self.repository = repository
        self.jack = jack
        self.rose = rose
        self.cal = cal
        self.walter = walter
        self.andrews = andrews

    async def chat(self, schema: SmithChatRequest) -> SmithChatResponse:
        logger.info(f"[SmithCaptainInteractor] chat 진입 | message={schema.message}")

        train_set               = await self.walter.get_train_set()
        test_set                = await self.walter.get_test_set()

        if train_set.empty:
            return SmithChatResponse(
                reply="데이터가 아직 없습니다. James 감독에게 CSV를 먼저 업로드해 달라고 하십시오.",
                model="none",
            )

        train_result: dict      = await self.jack.train_model(train_set)
        question: dict          = self.andrews.analyze_intent(schema.message)

        scores: dict = train_result.get("scores", {})
        if not scores:
            return SmithChatResponse(
                reply="모델 훈련에 실패했습니다. 데이터를 확인해 주십시오.",
                model="none",
            )

        best_model: str      = max(scores, key=lambda k: scores[k])
        best_accuracy: float = scores[best_model]
        intent: str          = question.get("intent", "UNKNOWN")

        reply = self._build_reply(intent, train_set, test_set, best_model, best_accuracy, scores)
        logger.info(f"[SmithCaptainInteractor] intent={intent} best_model={best_model} accuracy={best_accuracy:.4f}")
        return SmithChatResponse(reply=reply, model=best_model)

    # Kaggle Titanic 전체 데이터셋 기준 (훈련 891 + 테스트 418)
    _TOTAL_PASSENGERS    = 1_309
    _TOTAL_SURVIVED      = 500
    _TOTAL_DEAD          = 809

    def _build_reply(
        self,
        intent: str,
        train_set,
        test_set,
        best_model: str,
        best_accuracy: float,
        scores: dict,
    ) -> str:
        total    = self._TOTAL_PASSENGERS
        survived = self._TOTAL_SURVIVED
        dead     = self._TOTAL_DEAD
        rate     = survived / total * 100

        if intent == "STATISTICS":
            return (
                f"타이타닉 탑승 인원은 총 {total:,}명입니다.\n"
                f"생존자: {survived:,}명 ({rate:.1f}%), 사망자: {dead:,}명 ({100 - rate:.1f}%)"
            )

        if intent == "SURVIVAL_PREDICT":
            return (
                f"생존율은 {rate:.1f}% ({survived:,}명 / {total:,}명)입니다.\n"
                f"ML 예측 모델 {best_model}의 정확도는 {best_accuracy:.1%}입니다."
            )

        if intent == "PASSENGER_SEARCH":
            return (
                f"타이타닉 탑승 인원은 총 {total:,}명입니다.\n"
                f"생존자 {survived:,}명, 사망자 {dead:,}명입니다."
            )

        if intent == "MODEL_TRAIN":
            score_lines = ", ".join(
                f"{m} {a:.1%}" for m, a in sorted(scores.items(), key=lambda x: -x[1])
            )
            return (
                f"훈련 완료. 1위 모델: {best_model} ({best_accuracy:.1%})\n"
                f"전체 정확도: {score_lines}"
            )

        return (
            f"타이타닉에는 총 {total:,}명이 탑승했으며, "
            f"{survived:,}명({rate:.1f}%)이 생존하고 {dead:,}명이 사망했습니다."
        )

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name,
        ))
