"""Walter 출력 포트 — `walter_query` / `walter_command` → 저장소 경계."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class WalterPersistPayload:
    """쿼리·커맨드에서 변환된 업로드 행 묶음."""

    filename: str
    columns: list[str]
    rows: list[dict[str, Any]]


@runtime_checkable
class WalterRepositoryPort(Protocol):
    async def save_upload(
        self,
        *,
        filename: str,
        columns: list[str],
        rows: list[dict[str, Any]],
    ) -> int:
        """변환된 업로드 데이터를 저장하고 저장된 행 수를 반환합니다."""

    async def fetch_all(self) -> list[dict[str, Any]]:
        """저장된 전체 행을 API 응답 형식(PascalCase + gender)으로 반환합니다."""


async def submit_persist_upload(
    repository: WalterRepositoryPort,
    payload: WalterPersistPayload,
) -> int:
    """`walter_command` → 출력 포트 → `walter_pg_repository`."""
    logger.info(
        "[walter_repository] 저장 전달 — filename=%s rows=%s columns=%s → %s",
        payload.filename,
        len(payload.rows),
        ", ".join(payload.columns),
        type(repository).__name__,
    )
    row_count = await repository.save_upload(
        filename=payload.filename,
        columns=payload.columns,
        rows=payload.rows,
    )
    logger.info(
        "[walter_repository] 저장 응답 — filename=%s saved_rows=%s",
        payload.filename,
        row_count,
    )
    return row_count


async def submit_fetch_all_passengers(
    repository: WalterRepositoryPort,
) -> list[dict[str, Any]]:
    """`walter_query` → 출력 포트 → `walter_pg_repository`."""
    logger.info(
        "[walter_repository] 조회 전달 — fetch_all → %s",
        type(repository).__name__,
    )
    rows = await repository.fetch_all()
    logger.info("[walter_repository] 조회 응답 — rows=%s", len(rows))
    return rows
