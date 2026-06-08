from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import JamesDirectorRecordsSchema

logging.getLogger(__name__).setLevel(logging.WARNING)


class JamesDirectorUseCase(ABC):
    """CSV 파싱 이후 애플리케이션 레이어 (로그·저장·도메인 규칙)."""

    @abstractmethod
    async def receive_uploaded_records(self, schema: JamesDirectorRecordsSchema) -> None:
        """라우터가 `JamesDirectorRecordsSchema` 를 넘긴 뒤 호출."""
        ...
