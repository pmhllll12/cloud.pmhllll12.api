"""타이타닉 커맨드 HTTP 인바운드 어댑터 (V1)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.schemas.titanic_request import TitanicPassengerRowRequest
from titanic.adapter.inbound.schemas.titanic_response import TitanicCommandResponse
from titanic.app.ports.input.titanic_command_port import TitanicCommandPort
from titanic.app.use_cases.titanic_command_impl import TitanicCommandImpl

router = APIRouter()


def get_titanic_command_port() -> TitanicCommandPort:
    return TitanicCommandImpl()


@router.post(
    "/commands/passenger-row",
    response_model=TitanicCommandResponse,
    summary="타이타닉 승객 한 행(문자열 스키마) 제출",
)
def post_titanic_passenger_row(
    body: TitanicPassengerRowRequest,
    port: Annotated[TitanicCommandPort, Depends(get_titanic_command_port)],
) -> TitanicCommandResponse:
    """헥사고날 구조: HTTP → 커맨드 포트 → 유스케이스 구현."""
    return port.handle_passenger_row(body)
