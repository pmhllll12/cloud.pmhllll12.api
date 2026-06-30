from __future__ import annotations

from abc import ABC, abstractmethod

from community.adapter.inbound.api.schemas.juso_schemas import JusoResponse, JusoSchema


class JusoUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: JusoSchema) -> JusoResponse:
        raise NotImplementedError
