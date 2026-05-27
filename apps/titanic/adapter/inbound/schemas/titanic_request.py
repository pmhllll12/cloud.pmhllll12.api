"""Titanic CSV 한 행에 대응하는 인바운드 요청 스키마 (모든 값은 str, Sex → Gender)."""

from __future__ import annotations

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class TitanicPassengerRowRequest(BaseModel):
    """스프레드시트 헤더(A~L)와 동일한 컬럼. 원래 `Sex` 열은 API 필드명 `Gender` 로 받습니다."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "PassengerId": "1",
                "Survived": "1",
                "Pclass": "3",
                "Name": "Braund, Mr. Owen Harris",
                "Gender": "male",
                "Age": "22",
                "SibSp": "1",
                "Parch": "0",
                "Ticket": "A/5 21171",
                "Fare": "7.25",
                "Cabin": "",
                "Embarked": "S",
            }
        },
    )

    passenger_id: str = Field(..., alias="PassengerId")
    survived: str = Field(..., alias="Survived")
    pclass: str = Field(..., alias="Pclass")
    name: str = Field(..., alias="Name")
    gender: str = Field(
        ...,
        validation_alias=AliasChoices("Gender", "gender", "Sex"),
        serialization_alias="Gender",
        description="원 CSV 컬럼 Sex → 스키마 필드 gender (입력은 Gender·gender·Sex 허용)",
    )
    age: str = Field(..., alias="Age")
    sib_sp: str = Field(..., alias="SibSp")
    parch: str = Field(..., alias="Parch")
    ticket: str = Field(..., alias="Ticket")
    fare: str = Field(..., alias="Fare")
    cabin: str = Field(..., alias="Cabin")
    embarked: str = Field(..., alias="Embarked")
