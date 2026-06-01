"""James CSV 업로드 — 라우터 → 입력 포트(`receive_uploaded_records`) → 출력 포트."""

from __future__ import annotations

import logging
from contextvars import ContextVar

from titanic.adapter.inbound.api.schemas.james_response import JamesUploadResponse
from titanic.app.ports.input.james_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_repository import JamesRepository
from titanic.app.titanic_csv_parser import parse_titanic_csv

logger = logging.getLogger(__name__)

james_repository_ctx: ContextVar[JamesRepositoryPort | None] = ContextVar(
    "james_repository_port",
    default=None,
)


class JamesDirectorInteractor(JamesDirectorUseCase):
    """HTTP에서 읽은 CSV 바이트를 파싱·Sex→gender·Neon 저장까지 처리합니다."""

    @staticmethod
    def _repository() -> JamesRepositoryPort:
        repo = james_repository_ctx.get()
        if repo is None:
            raise RuntimeError("JamesRepositoryPort 가 컨텍스트에 설정되지 않았습니다.")
        return repo

    async def receive_uploaded_records(self, input_data: JamesUploadInput) -> JamesUploadResponse:
        """라우터 `upload_titanic_csv` 에서 `submit_csv_upload` 로 넘어온 페이로드 처리."""
        payload = parse_titanic_csv(input_data.content, input_data.filename)
        row_count = await submit_persist_upload(
            JamesCommand._repository(),
            JamesPersistPayload(
                filename=input_data.filename,
                columns=list(payload["columns"]),
                rows=list(payload["rows"]),
            ),
        )
        logger.info(
            "[james_command] 애플리케이션 — CSV 파싱·Sex→gender·저장 완료 filename=%s rows=%s",
            input_data.filename,
            row_count,
        )
        return JamesUploadResponse(
            ok=True,
            message=str(payload["message"]),
            filename=input_data.filename,
            row_count=row_count,
            columns=list(payload["columns"]),
            preview=list(payload["preview"]),
            rows=list(payload["rows"]),
        )
