from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from community.adapter.inbound.api.schemas import EmailSendRequest, EmailSendResponse  # noqa: E501
from community.adapter.outbound.n8n_email_client import N8nEmailClient
from community.dependencies.providers import get_n8n_email_client

email_router = APIRouter(tags=["community-email"])


@email_router.post("/email/send", response_model=EmailSendResponse)
async def send_email(
    body: EmailSendRequest,
    client: N8nEmailClient = Depends(get_n8n_email_client),
) -> EmailSendResponse:
    """주제를 받아 EXAONE가 이메일을 작성하고 n8n을 통해 Gmail로 발송합니다."""
    ok = await client.send_email(to_email=body.to_email, topic=body.topic)
    if not ok:
        raise HTTPException(status_code=502, detail="n8n 이메일 발송 실패. n8n 워크플로우 상태를 확인하세요.")
    return EmailSendResponse(ok=True, message=f"{body.to_email} 으로 발송 요청 완료")
