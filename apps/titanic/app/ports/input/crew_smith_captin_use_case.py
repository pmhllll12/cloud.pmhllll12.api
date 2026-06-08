from __future__ import annotations
from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_smith_captin_schemas import SmithCaptainSchema
from titanic.app.dtos.crew_smith_captin_dto import SmithCaptainResponse

class SmithCaptainUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 메소드'''
        pass