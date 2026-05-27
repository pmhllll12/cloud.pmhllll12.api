"""커맨드 처리 결과(인바운드 어댑터 응답 DTO)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TitanicCommandResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ok": True,
                "message": "등록 요청을 수락했습니다.",
                "row": {"PassengerId": "1", "Gender": "male"},
            }
        },
    )

    ok: bool = Field(..., description="처리 성공 여부")
    message: str = Field(..., description="사람이 읽을 수 있는 메시지")
    row: dict[str, str] = Field(
        default_factory=dict,
        description="수신 행 에코 (JSON 키는 PascalCase, Sex 대신 Gender)",
    )
