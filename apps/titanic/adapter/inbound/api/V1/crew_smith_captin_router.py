import asyncio
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from core.matrix.vault_keymaker_secret_manager import MissingApiKeyError, format_gemini_error, keymaker
from titanic.adapter.inbound.api.schemas.crew_smith_captin_schemas import (
    SmithCaptainSchema,
    SmithChatRequest,
    SmithChatResponse,
)
from titanic.app.dtos.crew_smith_captin_dto import SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captin_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captin_provider import get_smith_captain_use_case

'''
스미스 선장 (Captain Edward John Smith)
타이타닉의 총책임자. 침몰하는 배와 운명을 함께한 명장.
전체 승객 현황(생존/사망 통계)을 관장하는 마스터 역할.

추천 파일명: smith_captain_router.py (또는 smith_wheel_router.py)
'''

smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])

_SMITH_TITANIC_PROMPT = """[역할]
당신은 RMS 타이타닉(RMS Titanic)의 선장 에드워드 존 스미스(Edward John Smith, 1850–1912)입니다.
격조 있고 차분한 말투로, 당시 항해와 침몰 전후의 상황을 '제 입장에서' 이야기합니다.

[지침]
- 한국어로 답합니다. 문단은 짧게 나눕니다.
- 타이타닉·백년제선·해상 안전·1912년 역사와 관련된 질문에 우선 집중합니다.
- 기록·조사로 알려진 사실과 소설·영화·도시전설을 구분해 말합니다.
- 현대 선박의 실제 운항 지시·위법·욕설 요청은 정중히 거절합니다.
- 질문이 주제와 멀면 짧게 답한 뒤 타이타닉 이야기로 자연스럽게 이어갑니다.

[승객의 말]
"""


def _extract_gemini_text(response: Any) -> str:
    try:
        text = (response.text or "").strip()
    except ValueError:
        text = ""
    if text:
        return text
    if response.candidates:
        parts = response.candidates[0].content.parts
        chunks = [getattr(p, "text", "") or "" for p in parts]
        return "".join(chunks).strip()
    return ""


@smith_captain_router.post("/chat")
async def chat(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
) -> SmithCaptainResponse:
   return None


@smith_captain_router.get("/myself")
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
) -> SmithCaptainResponse:
    return await james.introduce_myself(
        SmithCaptainSchema(
            id=7,
            name="스미스 선장 (Captain Edward John Smith)",
        )
    )
