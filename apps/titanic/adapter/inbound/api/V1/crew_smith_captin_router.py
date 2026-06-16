import logging
from fastapi import APIRouter, Depends

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


@smith_captain_router.post("/chat", response_model=SmithChatResponse)
async def smith_titanic_chat(
    schema: Annotated[SmithChatRequest, Body()],
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
) -> SmithChatResponse:
    for msg in schema.messages:
        logger.info("[smith/chat]" message from {msg.role}: {msg.content}")
    """유스케이스로 위임 (`GEMINI_API_KEY` 필요)."""
    return await smith.chat(schema)


@smith_captain_router.get("/myself")
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
) -> SmithCaptainResponse:
    return await smith.introduce_myself(
        SmithCaptainSchema(
            id=7,
            name="스미스 선장 (Captain Edward John Smith)",
        )
    )
