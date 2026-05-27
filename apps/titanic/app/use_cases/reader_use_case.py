"""Titanic 데모 데이터셋 저장소."""

from __future__ import annotations

import pandas as pd

from titanic.app.demo_data import titanic_demo_dataframe


class TitanicDatasetRepository:
    """데모 데이터프레임을 반환하는 저장소."""

    def load_all(self) -> pd.DataFrame:
        return titanic_demo_dataframe()
