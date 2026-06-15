from __future__ import annotations

import asyncio
import logging
from typing import Any

from fastapi import HTTPException

from core.matrix.vault_keymaker_secret_manager import MissingApiKeyError, format_gemini_error, keymaker
from titanic.adapter.inbound.api.schemas.crew_smith_captin_schemas import (
    SmithCaptainSchema,
    SmithChatRequest,
    SmithChatResponse,
)
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schemas import JackTrainerSchema
from titanic.adapter.inbound.api.schemas.passenger_rose_model_schemas import RoseModelSchema
from titanic.app.dtos.crew_smith_captin_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse
from titanic.app.ports.input.crew_smith_captin_use_case import SmithCaptainUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captin_repository import SmithCaptainRepository

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


logger = logging.getLogger(__name__)


class SmithCaptainInteractor(SmithCaptainUseCase):
    """선장 유스케이스 — 잭·로즈와 조합 호출 가능."""

    def __init__(
        self,
        repository: SmithCaptainRepository,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
    ) -> None:
        self.repository = repository
        self._jack = jack
        self._rose = rose

    async def introduce_crew_with_passengers(
        self,
        smith_schema: SmithCaptainSchema,
        jack_schema: JackTrainerSchema,
        rose_schema: RoseModelSchema,
    ) -> tuple[SmithCaptainResponse, JackTrainerResponse, RoseModelResponse]:
        smith_r = await self.introduce_myself(smith_schema)
        jack_r = await self._jack.introduce_myself(jack_schema)
        rose_r = await self._rose.introduce_myself(rose_schema)
        return smith_r, jack_r, rose_r

    async def chat(self, body: SmithChatRequest) -> SmithChatResponse:
        logger.info("[SmithCaptainInteractor/chat] message=%r", body.message)
        prompt = _SMITH_TITANIC_PROMPT + body.message.strip()

        def _generate() -> tuple[Any, str]:
            return keymaker.generate_content(prompt)

        try:
            response, model_used = await asyncio.to_thread(_generate)
        except MissingApiKeyError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except Exception as exc:
            status, detail = format_gemini_error(exc)
            raise HTTPException(status_code=status, detail=detail) from exc

        reply = _extract_gemini_text(response)
        if not reply:
            raise HTTPException(
                status_code=502,
                detail="모델이 비어 있는 응답을 반환했습니다.",
            )
        return SmithChatResponse(reply=reply, model=model_used)
