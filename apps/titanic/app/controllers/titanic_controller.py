from __future__ import annotations

import pandas as pd

from titanic.app.services.titanic_service import TitanicService


class TitanicController:
    """main.py 의 Titanic 엔드포인트용 얇은 컨트롤러."""

    def __init__(self) -> None:
        self._service = TitanicService()

    def get_data(self) -> pd.DataFrame:
        return self._service.load_frame()

    def get_count(self) -> int:
        return self._service.row_count()

    def has_decision_tree_model(self) -> bool:
        try:
            self._service.train_decision_tree_metrics()
        except (FileNotFoundError, ValueError):
            return False
        return True

    def get_model_name_and_accuracy(self) -> dict[str, object]:
        return self._service.train_decision_tree_metrics()
