from __future__ import annotations

from fastapi import APIRouter, Depends

from community.adapter.inbound.api.schemas.juso_schemas import JusoResponse, JusoSchema
from community.app.ports.input.juso_use_case import JusoUseCase
from community.dependencies.providers import get_juso_use_case

juso_router = APIRouter(prefix="/juso", tags=["juso"])


@juso_router.get("/myself", response_model=JusoResponse)
async def introduce_myself(
    use_case: JusoUseCase = Depends(get_juso_use_case),
) -> JusoResponse:
    return await use_case.introduce_myself(
        JusoSchema(id=2, name="주소록 관리자")
    )
