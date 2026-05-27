"""Titanic 승객 입력 검증."""

from __future__ import annotations

from typing import Any

import pandas as pd


class TitanicPassengerValidator:
    """POST /titanic/passengers 등에서 사용하는 단일 행 검증."""

    _EXPECTED_COLUMNS: tuple[str, ...] = (
        "Pclass",
        "Name",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "Ticket",
        "Fare",
        "Cabin",
        "Embarked",
    )

    def validate_row(self, row: dict[str, Any]) -> tuple[bool, list[str]]:
        errors: list[str] = []

        missing = [c for c in self._EXPECTED_COLUMNS if c not in row]
        if missing:
            errors.append(f"누락된 컬럼: {', '.join(missing)}")

        extra = [c for c in row if c not in self._EXPECTED_COLUMNS]
        if extra:
            errors.append(f"허용되지 않은 컬럼: {', '.join(extra)}")

        if errors:
            return False, errors

        try:
            pd.Series(row)
        except Exception as exc:  # noqa: BLE001
            return False, [f"값 형식 오류: {exc}"]

        return True, []
