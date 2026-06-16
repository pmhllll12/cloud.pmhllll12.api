from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schemas import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository


class WalterRoasterInteractor(WalterRoasterUseCase):
    def __init__(self, repository: WalterRoasterRepository) -> None:
        self.repository = repository

    def get_train_set(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        '''월터가 DB에서 train set만 가져오는 메소드'''

    def get_test_set(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        '''월터가 DB에서 test set만 가져오는 메소드'''
        pass

    def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        query = WalterRoasterQuery(id=schema.id, name=schema.name, memo=schema.memo)
        return self.repository.introduce_myself(query)
