"""James CSV 업로드 응답 DTO."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class JamesUploadResponse(BaseModel):
    ok: bool = Field(..., description="처리 성공 여부")
    message: str = Field(..., description="사람이 읽을 수 있는 메시지")
    filename: str = Field(..., description="업로드된 파일명")
    row_count: int = Field(..., description="데이터 행 수 (헤더 제외)")
    columns: list[str] = Field(..., description="변환 후 컬럼명 (Sex → gender, 원본과 동일 PascalCase)")
    preview: list[dict[str, Any]] = Field(
        default_factory=list,
        description="앞쪽 샘플 행 (최대 5행)",
    )
    rows: list[dict[str, Any]] = Field(
        default_factory=list,
        description="전체 행 (gender 컬럼 포함, DB에는 id 가 자동 부여)",
    )
