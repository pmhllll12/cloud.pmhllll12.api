"""Walter CSV 업로드·조회 입력 포트 — 라우터 ↔ 유스케이스 계약."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from titanic.adapter.inbound.api.schemas.walter_response import (
    WalterDataResponse,
    WalterUploadResponse,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class WalterUploadInput:
    """`walter_router` POST /upload 에서 수신한 CSV 페이로드."""

    content: bytes
    filename: str


@runtime_checkable
class WalterUseCasePort(Protocol):
    async def upload_titanic_csv(self, input_data: WalterUploadInput) -> WalterUploadResponse:
        """업로드 CSV를 Sex → gender 변환 후 저장합니다."""

    async def get_passenger_data(self) -> WalterDataResponse:
        """저장된 승객 데이터를 gender 컬럼 포함해 반환합니다."""


async def submit_csv_upload(
    port: WalterUseCasePort,
    *,
    content: bytes,
    filename: str,
) -> WalterUploadResponse:
    """라우터 → `WalterUploadInput` → `walter_query` 업로드."""
    input_data = WalterUploadInput(content=content, filename=filename.strip())
    logger.info(
        "[walter_use_case] 입력 포트 전달 — upload filename=%s bytes=%s → walter_query",
        input_data.filename,
        len(input_data.content),
    )
    result = await port.upload_titanic_csv(input_data)
    logger.info(
        "[walter_use_case] 입력 포트 응답 — upload filename=%s row_count=%s columns=%s",
        result.filename,
        result.row_count,
        ", ".join(result.columns),
    )
    return result


async def submit_passenger_data_query(port: WalterUseCasePort) -> WalterDataResponse:
    """라우터 GET /data → `walter_query` 조회."""
    logger.info("[walter_use_case] 입력 포트 전달 — fetch_all → walter_query")
    result = await port.get_passenger_data()
    logger.info(
        "[walter_use_case] 입력 포트 응답 — fetch row_count=%s columns=%s",
        result.row_count,
        ", ".join(result.columns),
    )
    return result
