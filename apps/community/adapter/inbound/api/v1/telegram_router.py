from __future__ import annotations

from fastapi import APIRouter, Depends

from community.adapter.inbound.api.schemas.telegram_schemas import TelegramResponse, TelegramSchema
from community.app.ports.input.telegram_use_case import TelegramUseCase
from community.dependencies.providers import get_telegram_use_case

telegram_router = APIRouter(prefix="/telegram", tags=["telegram"])


@telegram_router.get("/myself", response_model=TelegramResponse)
async def introduce_myself(
    use_case: TelegramUseCase = Depends(get_telegram_use_case),
) -> TelegramResponse:
    return await use_case.introduce_myself(
        TelegramSchema(id=4, name="텔레그램 관리자")
    )
