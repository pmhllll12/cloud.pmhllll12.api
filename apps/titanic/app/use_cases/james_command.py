"""James CSV 업로드 커맨드 — 입력 포트 `JamesUseCasePort` 구현."""

from __future__ import annotations

from titanic.adapter.inbound.api.schemas.james_response import JamesUploadResponse
from titanic.app.ports.input.james_use_case import JamesUseCasePort
from titanic.app.ports.output.james_repository import JamesRepositoryPort
from titanic.app.titanic_csv_parser import parse_titanic_csv


class JamesCommand(JamesUseCasePort):
    """업로드 CSV를 검증·변환한 뒤 출력 포트(저장소)로 전달합니다."""

    def __init__(self, repository: JamesRepositoryPort) -> None:
        self._repository = repository

    async def upload_titanic_csv(self, content: bytes, filename: str) -> JamesUploadResponse:
        payload = parse_titanic_csv(content, filename)
        row_count = await self._repository.save_upload(
            filename=filename,
            columns=payload["columns"],
            rows=payload["rows"],
        )
        payload["row_count"] = row_count
        return JamesUploadResponse(**payload)
