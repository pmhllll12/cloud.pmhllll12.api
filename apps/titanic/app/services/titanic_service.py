from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def _package_data_csv() -> Path:
    # titanic/app/services/titanic_service.py → …/titanic/data/titanic.csv
    return Path(__file__).resolve().parents[2] / "data" / "titanic.csv"


class TitanicService:
    """CSV 로드·간단 의사결정나무 학습."""

    def __init__(self, csv_path: Path | None = None) -> None:
        self._csv_path = csv_path or _package_data_csv()

    def load_frame(self) -> pd.DataFrame:
        if not self._csv_path.is_file():
            raise FileNotFoundError(
                f"Titanic CSV not found: {self._csv_path}. "
                "Add titanic/data/titanic.csv (Kaggle-style columns)."
            )
        return pd.read_csv(self._csv_path)

    def row_count(self) -> int:
        return len(self.load_frame())

    def train_decision_tree_metrics(self) -> dict[str, object]:
        df = self.load_frame()
        if "Survived" not in df.columns:
            raise ValueError("CSV must include a 'Survived' column.")

        y = df["Survived"].astype(int)
        X_raw = df.drop(columns=["Survived"], errors="ignore")
        X_raw = X_raw.drop(
            columns=[c for c in ("PassengerId", "Name", "Ticket", "Cabin") if c in X_raw.columns],
            errors="ignore",
        )
        X = pd.get_dummies(X_raw, drop_first=False)
        X = X.apply(pd.to_numeric, errors="coerce").fillna(0.0)

        if X.shape[1] == 0:
            raise ValueError("No usable feature columns after preprocessing.")

        stratify = y if y.nunique() > 1 else None
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=stratify
        )
        clf = DecisionTreeClassifier(max_depth=4, random_state=42)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        acc = float(accuracy_score(y_test, y_pred))

        return {
            "model": "DecisionTreeClassifier",
            "accuracy": round(acc, 4),
            "train_rows": int(len(X_train)),
            "test_rows": int(len(X_test)),
            "feature_count": int(X.shape[1]),
        }
