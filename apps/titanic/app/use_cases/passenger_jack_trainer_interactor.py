from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

from titanic.adapter.outbound.orm.passenger_rose_model_strategies import build_all_strategies
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schemas import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort

logger = logging.getLogger(__name__)


class JackTrainerInteractor:

    def __init__(self, repository: JackTrainerPort):
        self.repository = repository
        self._trained_strategies: dict = {}

    async def train_model(self, train_set: pd.DataFrame) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
        logger.info("[JackTrainerInteractor] 학습 파이프라인 시작")

        train = train_set.copy()

        # DB에서 모든 컬럼이 문자열로 오므로 수치형 컬럼을 float으로 변환
        for col in ("Age", "Fare", "SibSp", "Parch", "Survived"):
            if col in train.columns:
                train[col] = pd.to_numeric(train[col], errors="coerce")

        # 1. Label 분리
        y_label = train["Survived"].fillna(0).astype(int).tolist()
        train = train.drop("Survived", axis=1)

        # 2. 호칭 추출 및 Nominal 변환
        train["Title"] = train["Name"].str.extract(r"([A-Za-z]+)\.", expand=False)
        train["Title"] = train["Title"].replace(
            ["Capt", "Col", "Don", "Dr", "Major", "Rev", "Jonkheer", "Dona", "Mme"], "Rare"
        )
        train["Title"] = train["Title"].replace(["Countess", "Lady", "Sir"], "Royal")
        train["Title"] = train["Title"].replace({"Mlle": "Mr", "Ms": "Miss"})
        title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Royal": 5, "Rare": 6}
        train["Title"] = train["Title"].map(title_mapping).fillna(0).astype(int)

        # 3. 성별 Nominal 변환 (female=1, male=0)
        train["gender"] = train["gender"].map({"male": 0, "female": 1})

        # 4. 나이 구간 Ordinal 변환 및 결측치 처리
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        age_labels = ["Unknown", "Baby", "Child", "Teenager", "Student", "Young Adult", "Adult", "Senior"]
        age_title_mapping = {
            0: "Unknown", 1: "Baby", 2: "Child", 3: "Teenager",
            4: "Student", 5: "Young Adult", 6: "Adult", 7: "Senior",
        }
        age_mapping = {v: k for k, v in age_title_mapping.items()}

        train["Age"] = train["Age"].fillna(-0.5)
        train["AgeGroup"] = pd.cut(train["Age"], bins, labels=age_labels).astype(str)
        mask = train["AgeGroup"] == "Unknown"
        train.loc[mask, "AgeGroup"] = train.loc[mask, "Title"].map(age_title_mapping)
        train["AgeGroup"] = train["AgeGroup"].map(age_mapping).fillna(0).astype(int)

        # 5. 승선항 Nominal 변환
        train["Embarked"] = train["Embarked"].fillna("S").map({"S": 1, "C": 2, "Q": 3})

        # 6. 요금 Ordinal 변환 (train 기준 4분위 구간 정의)
        train["FareBand"] = (
            pd.qcut(train["Fare"], 4, labels=[1, 2, 3, 4], duplicates="drop")
            .fillna(1).astype(int)
        )

        # 7. 불필요 컬럼 드롭
        drop_cols = ["Name", "Age", "Fare", "Ticket", "Cabin", "PassengerId"]
        train = train.drop(columns=[c for c in drop_cols if c in train.columns])

        # 8. 훈련/검증 분리 (80/20)
        split = int(len(y_label) * 0.8)
        X_tr, X_val = train.values[:split].tolist(), train.values[split:].tolist()
        y_tr, y_val = y_label[:split], y_label[split:]

        # 9. 로즈의 전략으로 학습 + 검증 정확도 계산
        self._trained_strategies = {}
        trained_names: list[str] = []
        scores: dict[str, float] = {}
        for key, StrategyClass in build_all_strategies().items():
            strategy = StrategyClass()
            try:
                strategy.fit(X_tr, y_tr)
                preds = strategy.predict(X_val)
                accuracy = sum(p == t for p, t in zip(preds, y_val)) / len(y_val) if y_val else 0.0
                self._trained_strategies[key] = strategy
                trained_names.append(strategy.name)
                scores[strategy.name] = round(accuracy, 4)
                logger.info(f"[JackTrainerInteractor] {strategy.name} accuracy={accuracy:.4f}")
            except Exception as e:
                logger.warning(f"[JackTrainerInteractor] {key} 학습 실패 | error={e}")

        return {
            "train_samples": len(X_tr),
            "trained_models": trained_names,
            "trained_strategies": self._trained_strategies,
            "scores": scores,
        }

    

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(JackTrainerQuery(
            id=schema.id,
            name=schema.name,
        ))