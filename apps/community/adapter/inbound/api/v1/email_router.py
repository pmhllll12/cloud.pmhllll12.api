from __future__ import annotations

import asyncio
import logging
import os

import httpx
from fastapi import APIRouter, Depends, HTTPException

logger = logging.getLogger(__name__)

from community.adapter.inbound.api.schemas import EmailSendRequest, EmailSendResponse
from community.adapter.inbound.api.schemas.email_host_schemas import EmailHostResponse, EmailHostSchema
from community.app.dtos.send_email_dto import SendEmailCommand
from community.app.ports.input.email_host_use_case import EmailHostUseCase
from community.app.ports.input.send_email_use_case import SendEmailUseCase
from community.dependencies.providers import get_email_host_use_case, get_send_email_use_case
from ontology.app.ports.input.judge_use_case import JudgeUseCase
from ontology.dependencies.providers import get_judge_use_case
from ontology.domain.evidence import Evidence

email_router = APIRouter(tags=["community-email"])


@email_router.post("/email/send", response_model=EmailSendResponse)
async def send_email(
    body: EmailSendRequest,
    use_case: SendEmailUseCase = Depends(get_send_email_use_case),
    judge: JudgeUseCase = Depends(get_judge_use_case),
) -> EmailSendResponse:
    """주제를 받아 스팸 판정 후 EXAONE가 이메일을 작성하고 n8n을 통해 Gmail로 발송합니다."""
    evidence = Evidence(
        source_app="community",
        signals={
            "to_email": body.to_email,
            "topic": body.topic,
            "context": (
                "사용자가 관리자 대시보드에서 직접 입력한 이메일 발송 요청입니다. "
                "스팸 기준: 광고·홍보 문구 포함, 악성 URL 포함, 대량 발송 의심 문구. "
                "일반 업무·인사 메시지(예: 안녕, 회의 안내, 일정 공유)는 정상(HAM)으로 판정하세요."
            ),
        },
    )
    verdict = await judge.evaluate(evidence)
    if verdict.is_spam:
        raise HTTPException(
            status_code=400,
            detail=f"스팸으로 판정된 요청입니다. 사유: {verdict.reason}",
        )

    result = await use_case.send(SendEmailCommand(to_email=body.to_email, topic=body.topic))
    if not result.ok:
        raise HTTPException(status_code=502, detail="n8n 이메일 발송 실패. n8n 워크플로우 상태를 확인하세요.")

    # 텔레그램 알림 (비동기 fire-and-forget)
    asyncio.create_task(_notify_telegram(body.to_email, body.topic))

    return EmailSendResponse(ok=True, message=result.message)


async def _notify_telegram(to_email: str, topic: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("DEVELOPER_CHAT_ID", "")
    if not token or not chat_id:
        return
    text = f"✅ 이메일 발송 완료\n📧 수신자: {to_email}\n📝 주제: {topic}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": text},
            )
        logger.info("[email/send] telegram notify to=%s ok", chat_id)
    except Exception as exc:
        logger.warning("[email/send] telegram notify failed: %s", exc)


@email_router.get("/email/myself", response_model=EmailHostResponse)
async def introduce_myself(
    use_case: EmailHostUseCase = Depends(get_email_host_use_case),
) -> EmailHostResponse:
    return await use_case.introduce_myself(
        EmailHostSchema(id=5, name="이메일 관리자")
    )
