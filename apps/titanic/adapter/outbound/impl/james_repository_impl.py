"""James 업로드 저장소 — 메모리 구현 (후속: DB·파일 어댑터로 교체)."""

from __future__ import annotations

from typing import Any

from titanic.app.ports.output.james_repository import JamesRepositoryPort


class JamesRepositoryImpl(JamesRepositoryPort):
    """업로드마다 최신 스냅샷을 메모리에 보관합니다."""

    _latest: dict[str, Any] | None = None

    async def save_upload(
        self,
        *,
        filename: str,
        columns: list[str],
        rows: list[dict[str, Any]],
    ) -> int:
        JamesRepositoryImpl._latest = {
            "filename": filename,
            "columns": columns,
            "rows": rows,
        }
        return len(rows)

    async def fetch_page(
        self,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        if JamesRepositoryImpl._latest is None:
            return [], 0
        rows = JamesRepositoryImpl._latest.get("rows") or []
        if not isinstance(rows, list):
            return [], 0
        total = len(rows)
        start = (page - 1) * page_size
        chunk = rows[start : start + page_size]
        return chunk, total

    @classmethod
    def get_latest(cls) -> dict[str, Any] | None:
        return cls._latest
