from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

# 포트 모듈은 INFO 로그를 쓰지 않음(설정 순서와 무관하게 import 시점에 고정).
logging.getLogger(__name__).setLevel(logging.WARNING)


class JamesRepository(ABC):
    @abstractmethod
    async def save_all(self, records: list[dict[str, Any]]) -> int:
        ...


@dataclass(frozen=True, slots=True)
class JamesPersistPayload:
    """커맨드에서 변환된 업로드 행 묶음."""

    filename: str
    columns: list[str]
    rows: list[dict[str, Any]]


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


async def submit_persist_upload(
    repository: JamesRepositoryPort,
    payload: JamesPersistPayload,
) -> int:
    """`JamesCommand` → 출력 포트 → `JamesPgRepository`."""
    row_count = await repository.save_upload(
        filename=payload.filename,
        columns=payload.columns,
        rows=payload.rows,
    )
    return row_count
