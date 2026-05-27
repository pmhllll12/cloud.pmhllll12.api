"""Titanic 데모 데이터셋 기반 서비스."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from titanic.app.demo_data import titanic_demo_dataframe


class TitanicService:
    """Titanic 데모 데이터셋 로딩 및 간단한 ML 지표."""

    def load_frame(self) -> pd.DataFrame:
        return titanic_demo_dataframe()

    def row_count(self) -> int:
        return int(len(self.load_frame()))

    def train_decision_tree_metrics(self) -> dict[str, Any]:
        df = self.load_frame()
        if df.empty:
            return {
                "message": "데이터가 없습니다.",
                "accuracy": None,
                "classification_report": None,
                "confusion_matrix": None,
            }

        target = "Survived"
        drop_cols = {"PassengerId", "Name", "Ticket", "Cabin", "Embarked"}
        feature_cols = [c for c in df.columns if c not in drop_cols and c != target]

        X = df[feature_cols]
        y = df[target]

        numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
        categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

        numeric_transformer = Pipeline(
            steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
        )
        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features),
            ]
        )

        clf = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", DecisionTreeClassifier(random_state=42)),
            ]
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        acc = float(accuracy_score(y_test, y_pred))
        report = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred).tolist()

        return {
            "message": "Decision Tree 학습 완료",
            "accuracy": acc,
            "classification_report": report,
            "confusion_matrix": cm,
        }
