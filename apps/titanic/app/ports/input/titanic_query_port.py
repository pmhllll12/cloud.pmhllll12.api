"""애플리케이션 코어가 노출하는 타이타닉 조회(쿼리) 입력 포트."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class TitanicQueryPort(Protocol):
    def get_problem_payload(self) -> dict[str, object]:
        """문제 정의·스키마 힌트(JSON 직렬화 가능 dict)."""

    def get_passenger_data_records(self) -> list[dict[str, object]]:
        """탑승객 데이터 전체 행(레코드 배열)."""

    def get_passenger_count(self) -> int:
        """탑승객 행 수."""

    def has_decision_tree_model(self) -> bool:
        """의사결정나무 학습 가능 여부."""

    def get_model_metrics(self) -> dict[str, object]:
        """학습 메트릭(모델명·정확도 등)."""
