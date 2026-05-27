"""타이타닉 조회 유스케이스 — 기존 컨트롤러 로직을 서비스 호출로 캡슐화."""

from __future__ import annotations

from titanic.app.ports.input.titanic_query_port import TitanicQueryPort
from titanic.app.use_cases.titanic_service import TitanicService
from titanic.schemas import TitanicDatasetSchemaHint, TitanicProblemDefinition


class TitanicQueryImpl(TitanicQueryPort):
    def __init__(self, service: TitanicService | None = None) -> None:
        self._service = service or TitanicService()

    def get_problem_payload(self) -> dict[str, object]:
        return {
            "problem": TitanicProblemDefinition().model_dump(),
            "schema_hint": TitanicDatasetSchemaHint().model_dump(),
        }

    def get_passenger_data_records(self) -> list[dict[str, object]]:
        df = self._service.load_frame()
        return df.to_dict(orient="records")

    def get_passenger_count(self) -> int:
        return self._service.row_count()

    def has_decision_tree_model(self) -> bool:
        try:
            self._service.train_decision_tree_metrics()
        except ValueError:
            return False
        return True

    def get_model_metrics(self) -> dict[str, object]:
        return self._service.train_decision_tree_metrics()
