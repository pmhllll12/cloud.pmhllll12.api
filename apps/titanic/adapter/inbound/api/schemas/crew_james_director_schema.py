"""James director API — Titanic 데이터셋 CSV. `Sex` 열 → 필드 `gender`. 빈 셀은 허용."""

from __future__ import annotations

import json
from typing import Annotated, Any

from pydantic import (
    AliasChoices,
    BeforeValidator,
    BaseModel,
    ConfigDict,
    Field,
)


def _blank_to_none(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, str) and not v.strip():
        return None
    return v


def _blank_int_zero(v: Any) -> Any:
    """CSV 빈 칸 → 0 (SibSp, Parch 등)."""
    if v is None:
        return 0
    if isinstance(v, str) and not v.strip():
        return 0
    return v


def _blank_float_zero(v: Any) -> Any:
    """CSV 빈 칸 → 0.0 (Fare 등)."""
    if v is None:
        return 0.0
    if isinstance(v, str) and not v.strip():
        return 0.0
    return v


def _blank_str_default_empty(v: Any) -> Any:
    """빈 문자열은 그대로 빈 str (Ticket 등)."""
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    return v


IntFromCsv = Annotated[int, BeforeValidator(_blank_int_zero)]
FloatFromCsv = Annotated[float, BeforeValidator(_blank_float_zero)]
OptFloatFromCsv = Annotated[float | None, BeforeValidator(_blank_to_none)]
OptStrFromCsv = Annotated[str | None, BeforeValidator(_blank_to_none)]


class JamesDirectorPassengerRow(BaseModel):
    """승객 한 행. DictReader 가 넣는 빈 문자열(`""`)은 검증 전에 None/0 으로 정규화."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "PassengerId": 1,
                "Survived": 1,
                "Pclass": 3,
                "Name": "Braund, Mr. Owen Harris",
                "gender": "male",
                "Age": 22.0,
                "SibSp": 1,
                "Parch": 0,
                "Ticket": "A/5 21171",
                "Fare": 7.25,
                "Cabin": None,
                "Embarked": "S",
            }
        },
    )

    passenger_id: int = Field(..., alias="PassengerId", description="A열")
    survived: int = Field(..., alias="Survived", description="B열")
    pclass: int = Field(..., alias="Pclass", description="C열")
    name: str = Field(..., alias="Name", description="D열")
    gender: str = Field(
        ...,
        validation_alias=AliasChoices("gender", "Gender", "Sex"),
        serialization_alias="gender",
        description="E열 원본 Sex → gender",
    )
    age: OptFloatFromCsv = Field(None, alias="Age", description="F열 (공란 허용)")
    sib_sp: IntFromCsv = Field(..., alias="SibSp", description="G열")
    parch: IntFromCsv = Field(..., alias="Parch", description="H열")
    ticket: Annotated[str, BeforeValidator(_blank_str_default_empty)] = Field(
        default="",
        alias="Ticket",
        description="I열",
    )
    fare: FloatFromCsv = Field(..., alias="Fare", description="J열")
    cabin: OptStrFromCsv = Field(None, alias="Cabin", description="K열")
    embarked: OptStrFromCsv = Field(None, alias="Embarked", description="L열")


def preview_james_passenger_rows_json(rows: list[JamesDirectorPassengerRow], limit: int) -> str:
    """로그용: 상위 `limit` 행만 JSON."""
    sample: list[dict[str, object]] = []
    for r in rows[:limit]:
        name = r.name
        if len(name) > 60:
            name = name[:57] + "..."
        sample.append(
            {
                "PassengerId": r.passenger_id,
                "Survived": r.survived,
                "gender": r.gender,
                "Name": name,
            }
        )
    return json.dumps(sample, ensure_ascii=False)


class JamesDirectorRecordsSchema(BaseModel):
    """업로드 CSV 파싱 결과 — 파일명 + 승객 행 목록."""

    filename: str = Field(..., description="업로드된 CSV 파일명")
    rows: list[JamesDirectorPassengerRow] = Field(
        default_factory=list,
        description="검증·변환된 승객 행",
    )


class JamesDirectorUploadResponse(BaseModel):
    """`/upload` 응답."""

    ok: bool = True
    message: str = Field(default="", description="처리 메시지")
    filename: str = Field(default="", description="수신 파일명")
    row_count: int = Field(default=0, description="데이터 행 수 (헤더 제외)")
    note: str = Field(default="", description="추가 안내")


class JamesDirectorPassengersListResponse(BaseModel):
    """`/passengers` 목록 응답 (스텁)."""

    ok: bool = True
    items: list[JamesDirectorPassengerRow] = Field(default_factory=list)
    note: str = Field(default="", description="stub")


# 이전 이름 호환
TitanicRecordsSchema = JamesDirectorPassengerRow

__all__ = [
    "JamesDirectorPassengerRow",
    "JamesDirectorRecordsSchema",
    "JamesDirectorPassengersListResponse",
    "JamesDirectorUploadResponse",
    "TitanicRecordsSchema",
    "preview_james_passenger_rows_json",
]
