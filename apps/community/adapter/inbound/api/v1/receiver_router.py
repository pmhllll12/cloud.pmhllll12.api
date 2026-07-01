from __future__ import annotations

import logging
from collections import deque
from datetime import datetime

from fastapi import APIRouter

from community.adapter.inbound.api.schemas.email_incoming_schemas import (
    EmailIncomingRequest,
    EmailIncomingResponse,
)

receiver_router = APIRouter(prefix="/receiver", tags=["community-receiver"])
logger = logging.getLogger(__name__)

_log: deque[dict] = deque(maxlen=100)


@receiver_router.post("/incoming", response_model=EmailIncomingResponse)
async def receive_incoming_email(body: EmailIncomingRequest) -> EmailIncomingResponse:
    """n8n Gmail Trigger가 새로 도착한 메일을 수신합니다."""
    entry = {
        "received_at": datetime.now().isoformat(),
        "subject": body.subject,
        "from": body.from_,
        "to": body.to,
        "body": body.body,
    }
    _log.appendleft(entry)
    logger.info("[receiver/incoming] subject=%r from=%r", body.subject, body.from_)
    return EmailIncomingResponse(ok=True, message="received")


@receiver_router.get("/logs")
async def get_received_logs() -> list[dict]:
    """수신된 메일 로그를 최신순으로 반환합니다 (최대 100건, 서버 재시작 시 초기화)."""
    return list(_log)
