"""Walter 조회·라우터 → 입력 포트 전달 유스케이스."""

from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.walter_response import (
    WalterDataResponse,
    WalterUploadResponse,
)
from titanic.app.ports.input.walter_use_case import WalterUploadInput, WalterUseCasePort
from titanic.app.ports.output.walter_repository import (
    WalterRepositoryPort,
    submit_fetch_all_passengers,
)
from titanic.app.titanic_csv_parser import API_COLUMNS
from titanic.app.use_cases.walter_command import WalterCommand

logger = logging.getLogger(__name__)


class WalterQuery(WalterUseCasePort):
    """업로드(커맨드)와 DB 조회(쿼리)를 입력 포트 하나로 묶습니다."""

    def __init__(self, repository: WalterRepositoryPort) -> None:
        self._repository = repository
        self._command = WalterCommand(repository=repository)
        logger.info("[walter_query] 초기화 — repository=%s", type(repository).__name__)

    async def upload_titanic_csv(self, input_data: WalterUploadInput) -> WalterUploadResponse:
        logger.info(
            "[walter_query] 업로드 수신 — filename=%s bytes=%s → walter_command",
            input_data.filename,
            len(input_data.content),
        )
        result = await self._command.upload_titanic_csv(input_data)
        logger.info(
            "[walter_query] 업로드 완료 — filename=%s row_count=%s",
            result.filename,
            result.row_count,
        )
        return result

    async def get_passenger_data(self) -> WalterDataResponse:
        logger.info("[walter_query] 조회 수신 — → walter_repository.submit_fetch_all_passengers")
        rows = await submit_fetch_all_passengers(self._repository)
        logger.info("[walter_query] 조회 완료 — rows=%s", len(rows))
        return WalterDataResponse(
            ok=True,
            columns=list(API_COLUMNS),
            row_count=len(rows),
            rows=rows,
        )
