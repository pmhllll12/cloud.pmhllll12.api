"""Walter CSV 업로드 커맨드 (쓰기)."""

from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.walter_response import WalterUploadResponse
from titanic.app.ports.input.walter_use_case import WalterUploadInput
from titanic.app.ports.output.walter_repository import (
    WalterPersistPayload,
    WalterRepositoryPort,
    submit_persist_upload,
)
from titanic.app.titanic_csv_parser import parse_titanic_csv

logger = logging.getLogger(__name__)


class WalterCommand:
    def __init__(self, repository: WalterRepositoryPort) -> None:
        self._repository = repository

    async def upload_titanic_csv(self, input_data: WalterUploadInput) -> WalterUploadResponse:
        logger.info(
            "[walter_command] CSV 파싱 — filename=%s bytes=%s",
            input_data.filename,
            len(input_data.content),
        )
        payload = parse_titanic_csv(input_data.content, input_data.filename)
        logger.info(
            "[walter_command] Sex→gender 변환 완료 — rows=%s columns=%s → walter_repository",
            len(payload["rows"]),
            ", ".join(payload["columns"]),
        )
        row_count = await submit_persist_upload(
            self._repository,
            WalterPersistPayload(
                filename=input_data.filename,
                columns=list(payload["columns"]),
                rows=list(payload["rows"]),
            ),
        )
        logger.info(
            "[walter_command] 저장 완료 — filename=%s row_count=%s",
            input_data.filename,
            row_count,
        )
        return WalterUploadResponse(
            ok=True,
            message=str(payload["message"]),
            filename=input_data.filename,
            row_count=row_count,
            columns=list(payload["columns"]),
            preview=list(payload["preview"]),
        )
