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

    @classmethod
    def get_latest(cls) -> dict[str, Any] | None:
        return cls._latest
