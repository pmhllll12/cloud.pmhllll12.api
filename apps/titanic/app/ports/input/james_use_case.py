"""James CSV 업로드 입력 포트 — 어댑터가 애플리케이션 코어를 호출할 때 사용."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from titanic.adapter.inbound.api.schemas.james_response import JamesUploadResponse


@runtime_checkable
class JamesUseCasePort(Protocol):
    async def upload_titanic_csv(self, content: bytes, filename: str) -> JamesUploadResponse:
        """업로드된 CSV 바이트를 처리하고 Sex → gender 변환 결과를 반환합니다."""
