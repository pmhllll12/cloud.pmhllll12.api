from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from community.adapter.inbound.api.schemas import EmailSendRequest, EmailSendResponse
from community.app.dtos.send_email_dto import SendEmailCommand
from community.app.ports.input.send_email_use_case import SendEmailUseCase
from community.dependencies.providers import get_send_email_use_case
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
        signals={"to_email": body.to_email, "topic": body.topic},
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
    return EmailSendResponse(ok=True, message=result.message)
