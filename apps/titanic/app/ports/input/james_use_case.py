from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from titanic.adapter.inbound.api.schemas.james_response import JamesUploadResponse

# 포트 모듈은 INFO 로그를 쓰지 않음(설정 순서와 무관하게 import 시점에 고정).
logging.getLogger(__name__).setLevel(logging.WARNING)


class JamesUseCase(ABC):
    @abstractmethod
    async def receive_uploaded_records(self, input_data: JamesUploadInput) -> JamesUploadResponse:
        """라우터에서 넘긴 CSV 바이트를 파싱·변환·저장합니다."""


@dataclass(frozen=True, slots=True)
class JamesUploadInput:
    """`james_router` POST /upload 에서 수신한 CSV 페이로드."""

    content: bytes
    filename: str


@runtime_checkable
class JamesUseCasePort(Protocol):
    async def receive_uploaded_records(self, input_data: JamesUploadInput) -> JamesUploadResponse:
        ...


async def submit_csv_upload(
    port: JamesUseCasePort,
    *,
    content: bytes,
    filename: str,
) -> JamesUploadResponse:
    """라우터 → `JamesUploadInput` → `JamesCommand.receive_uploaded_records`."""
    input_data = JamesUploadInput(content=content, filename=filename.strip())
    return await port.receive_uploaded_records(input_data)
