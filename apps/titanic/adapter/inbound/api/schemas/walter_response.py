"""Walter CSV 업로드·조회 응답 DTO."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class WalterUploadResponse(BaseModel):
    ok: bool
    message: str
    filename: str
    row_count: int
    columns: list[str]
    preview: list[dict[str, Any]] = Field(default_factory=list)


class WalterDataResponse(BaseModel):
    ok: bool = True
    columns: list[str] = Field(default_factory=list)
    row_count: int = 0
    rows: list[dict[str, Any]] = Field(default_factory=list)
