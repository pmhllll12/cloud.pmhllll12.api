"""Walter Roaster — `schemas/crew_walter_roaster_schemas`."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schemas import WalterRoasterSchema
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUsecase
from titanic.dependencies.crew_walter_roaster import get_crew_walter_roaster_use_case

crew_walter_roaster_router = APIRouter(
    prefix="/walter-roaster",
    tags=["walter-roaster"],
)
walter_roaster_router = crew_walter_roaster_router


@crew_walter_roaster_router.get("/myself", response_model=WalterRoasterSchema)
def introduce_myself(
    walter: WalterRoasterUsecase = Depends(get_crew_walter_roaster_use_case),
) -> WalterRoasterSchema:
    schema = WalterRoasterSchema(
        id=2,
        name="Walter Nicholas",
        memo="타이타닉의 일등 항해사, 승객 명단 관리 담당",
    )
    walter.introduce_myself(schema)
    return schema
