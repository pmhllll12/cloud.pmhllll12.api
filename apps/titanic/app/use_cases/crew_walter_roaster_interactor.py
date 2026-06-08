import logging

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schemas import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUsecase
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository

logger = logging.getLogger(__name__)


class WalterRoasterInteractor(WalterRoasterUsecase):
    def __init__(self, repository: WalterRoasterRepository) -> None:
        self._repository = repository

    def introduce_myself(self, schema: WalterRoasterSchema) -> None:
        query = WalterRoasterQuery.from_schema(schema)

        logger.info("########################################################")
        logger.info("[월터 유스케이스] 라우터에서 받은 정보 → DTO")
        logger.info("ID: %s", query.id)
        logger.info("이름: %s", query.name)
        logger.info("메모: %s", query.memo)
        logger.info("########################################################")

        self._repository.introduce_myself(query)
