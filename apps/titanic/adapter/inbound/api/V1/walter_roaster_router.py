import logging

from fastapi import APIRouter

from titanic.adapter.inbound.api.schemas.walter_roaster_schemas import WalterRoasterSchema
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUsecase
from titanic.app.use_cases.walter_roster_interactor import WalterRoasterInteractor

logger = logging.getLogger(__name__)

walter_roaster_router = APIRouter(
    prefix="/walter-roaster",
    tags=["walter-roaster"],
)


@walter_roaster_router.get("/myself", response_model=WalterRoasterSchema)
async def introduce_myself(
    walter: WalterRoasterUsecase = Depends(get_walter_roaster_use_case)
)->WalterRoasterResponse:
    

    return await walter.introduce_myself(
        WalterRoasterSchema(
            id=2,
            name="Walter Nicholas",
            memo="타이타닉의 일등 항해사, 승객 명단 관리 담당"
        )
        )
