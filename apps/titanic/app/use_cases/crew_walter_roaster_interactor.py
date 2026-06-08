from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schemas import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository


class WalterRoasterInteractor(WalterRoasterUseCase):
    def __init__(self, repository: WalterRoasterRepository) -> None:
        self.repository = repository

    def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        query = WalterRoasterQuery(id=schema.id, name=schema.name, memo=schema.memo)
        return self.repository.introduce_myself(query)
