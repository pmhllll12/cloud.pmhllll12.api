"""James director API — Titanic 데이터셋 스프레드시트(A~L). CSV `Sex` 열 → 필드 `gender`."""

from __future__ import annotations

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class JamesDirectorPassengerRow(BaseModel):
    """승객 한 행: PassengerId … Embarked. 원본 E열 `Sex` 는 API에서 `gender` 로 다룹니다."""

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
        description="E열 원본 Sex → API 필드 gender (JSON 키는 gender 권장, Sex·Gender 입력 허용)",
    )
    age: float | None = Field(None, alias="Age", description="F열")
    sib_sp: int = Field(..., alias="SibSp", description="G열")
    parch: int = Field(..., alias="Parch", description="H열")
    ticket: str = Field(..., alias="Ticket", description="I열")
    fare: float = Field(..., alias="Fare", description="J열")
    cabin: str | None = Field(None, alias="Cabin", description="K열")
    embarked: str | None = Field(None, alias="Embarked", description="L열 (원본 공란 허용)")


class JamesDirectorRecordsSchema(BaseModel):
    """업로드 CSV를 파싱한 뒤 한 번에 담는 컨테이너 — 파일명 + 승객 행 목록."""

    filename: str = Field(..., description="업로드된 CSV 파일명")
    rows: list[JamesDirectorPassengerRow] = Field(
        default_factory=list,
        description="헤더 기준으로 검증·변환된 승객 행 (Sex → gender)",
    )


class JamesDirectorUploadResponse(BaseModel):
    """`/upload` 응답 — 파싱 요약."""

    ok: bool = True
    message: str = Field(default="", description="처리 메시지")
    filename: str = Field(default="", description="수신 파일명")
    row_count: int = Field(default=0, description="파싱된 데이터 행 수 (헤더 제외)")
    note: str = Field(
        default="",
        description="추가 안내 (예: DB 저장은 별도 파이프라인)",
    )


class JamesDirectorPassengersListResponse(BaseModel):
    """`/passengers` 목록 응답."""

    ok: bool = True
    items: list[JamesDirectorPassengerRow] = Field(default_factory=list)
    note: str = Field(default="stub — 페이지네이션·DB 연동 전")


__all__ = [
    "JamesDirectorPassengerRow",
    "JamesDirectorRecordsSchema",
    "JamesDirectorPassengersListResponse",
    "JamesDirectorUploadResponse",
]
