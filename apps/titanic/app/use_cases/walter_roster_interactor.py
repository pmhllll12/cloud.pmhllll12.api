import logging

from titanic.adapter.inbound.api.schemas.walter_roaster_schemas import WalterRoasterSchema
from titanic.adapter.outbound.pg.walter_roaster_pg_repository import WalterRoasterPgRepository
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUsecase
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository

logger = logging.getLogger(__name__)


class WalterRoasterInteractor(WalterRoasterUsecase):
    def __init__(self) -> None:
        pass

    def introduce_myself(self, schema: WalterRoasterSchema) -> None:
        """월터의 자기소개 메소드."""
        query = WalterRoasterQuery.from_schema(schema)

        logger.info("########################################################")
        logger.info("[월터 유스케이스] 라우터에서 받은 정보 → DTO")
        logger.info("ID: %s", query.id)
        logger.info("이름: %s", query.name)
        logger.info("메모: %s", query.memo)
        logger.info("########################################################")

        walter: WalterRoasterRepository = WalterRoasterPgRepository()
        walter.introduce_myself(query)
