"""James 업로드 데이터 출력 포트 — 커맨드가 변환한 CSV 행을 저장합니다."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class JamesRepositoryPort(Protocol):
    async def save_upload(
        self,
        *,
        filename: str,
        columns: list[str],
        rows: list[dict[str, Any]],
    ) -> int:
        """변환된 업로드 데이터를 저장하고 저장된 행 수를 반환합니다."""

    async def fetch_page(
        self,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        """승객 목록 한 페이지와 전체 행 수를 반환합니다."""
