"""James 승객 목록(페이지네이션) 응답 DTO."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class JamesPassengersPageResponse(BaseModel):
    ok: bool = True
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1)
    total_count: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=0)
    columns: list[str]
    items: list[dict[str, Any]]
