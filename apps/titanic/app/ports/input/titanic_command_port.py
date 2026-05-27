"""애플리케이션 코어가 호출하는 타이타닉 커맨드 입력 포트."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from titanic.adapter.inbound.schemas.titanic_request import TitanicPassengerRowRequest
from titanic.adapter.inbound.schemas.titanic_response import TitanicCommandResponse


@runtime_checkable
class TitanicCommandPort(Protocol):
    def handle_passenger_row(self, row: TitanicPassengerRowRequest) -> TitanicCommandResponse:
        """승객 한 행(문자열 스키마)을 처리합니다."""
