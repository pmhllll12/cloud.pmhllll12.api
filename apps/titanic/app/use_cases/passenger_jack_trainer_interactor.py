from __future__ import annotations

import asyncio
import logging
from typing import Any

from kiwipiepy import Kiwi

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schemas import JackTrainerSchema
from titanic.app.demo_data import titanic_demo_dataframe
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainRepository
from titanic.app.use_cases.passenger_rose_model_interactor import STRATEGY_REGISTRY, create_strategy

logger = logging.getLogger(__name__)


def prepare_titanic_features():
    """`_docs/titanic-algorithm.md` 1장: Pclass·Sex·Age·Fare 등 특성 변수로
    Survived(목적 변수)를 예측한다. 데모 데이터셋이라 결측치 보정만 최소로 처리.
    """
    df = titanic_demo_dataframe()
    features = df[["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]].copy()
    features["Sex"] = features["Sex"].map({"male": 0, "female": 1})
    features["Embarked"] = features["Embarked"].astype("category").cat.codes
    features["Age"] = features["Age"].fillna(features["Age"].median())
    return features, df["Survived"]


class JackTrainerInteractor(JackTrainerUseCase):
    def __init__(self, repository: JackTrainRepository, kiwi: Kiwi | None = None) -> None:
        self.repository = repository
        self.kiwi = kiwi if kiwi is not None else Kiwi()

    async def train_model(self, train_set) -> dict[str, Any]:
        """로즈가 제안할 모델들을 훈련시키는 메소드"""

        features = []
        target = []
        for row in train_set:
            sex_value = 1 if row["Sex"] == "female" else 0
            embarked_map = {"S": 0, "C": 1, "Q": 2}
            embarked_value = embarked_map.get(row["Embarked"], -1)

            features.append([
                row["Pclass"],
                sex_value,
                row["Age"],
                row["SibSp"],
                row["Parch"],
                row["Fare"],
                embarked_value,
            ])
            target.append(row["Survived"])

        scores = {}
        models = {}
        for name in STRATEGY_REGISTRY:
            strategy = create_strategy(name)
            strategy.fit(features, target)
            predictions = strategy.predict(features)

            correct = 0
            for predicted, actual in zip(predictions, target):
                if predicted == actual:
                    correct = correct + 1
            accuracy = correct / len(target)

            scores[name] = accuracy
            models[name] = strategy

        recommended = max(scores, key=scores.get)
        logger.info(
            "[JackTrainerInteractor/train_model] scores=%s recommended=%s",
            scores, recommended,
        )

        return {"scores": scores, "recommended": recommended, "models": models}


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
