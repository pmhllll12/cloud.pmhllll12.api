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
async def introduce_myself() -> WalterRoasterSchema:
    """월터 기본 프로필을 반환하고 유스케이스·저장소 체인을 실행합니다."""
    schema = WalterRoasterSchema()

    logger.info("########################################################")
    logger.info("[월터 라우터] 월터의 자기소개 API 호출")
    logger.info("ID: %s", schema.id)
    logger.info("이름: %s", schema.name)
    logger.info("메모: %s", schema.memo)
    logger.info("########################################################")

    walter: WalterRoasterUsecase = WalterRoasterInteractor()
    walter.introduce_myself(schema)

    return schema
