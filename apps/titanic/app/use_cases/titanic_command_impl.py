"""타이타닉 커맨드 유스케이스 구현 — 입력 포트 구현체."""

from __future__ import annotations

from titanic.adapter.inbound.api.schemas.titanic_request import TitanicPassengerRowRequest
from titanic.adapter.inbound.api.schemas.titanic_response import TitanicCommandResponse
from titanic.app.ports.input.titanic_command_port import TitanicCommandPort


class TitanicCommandImpl(TitanicCommandPort):
    """현재는 영속화 없이 검증된 페이로드를 에코합니다(후속: 저장소·도메인 연동)."""

    def handle_passenger_row(self, row: TitanicPassengerRowRequest) -> TitanicCommandResponse:
        payload = row.model_dump(mode="json", by_alias=True)
        # 모든 필드가 str 이므로 JSON 직렬화 시 그대로 str 유지
        flat: dict[str, str] = {k: str(v) for k, v in payload.items()}
        return TitanicCommandResponse(
            ok=True,
            message="등록 요청을 수락했습니다.",
            row=flat,
        )
