from __future__ import annotations

from community.adapter.inbound.api.schemas.juso_schemas import JusoResponse, JusoSchema
from community.app.dtos.juso_dto import JusoQuery
from community.app.ports.input.juso_use_case import JusoUseCase
from community.domain.juso import Juso


class JusoInteractor(JusoUseCase):
    async def introduce_myself(self, schema: JusoSchema) -> JusoResponse:
        query = JusoQuery(id=schema.id, name=schema.name)
        juso = Juso.default()
        return JusoResponse(
            id=query.id,
            name=juso.name,
            role=juso.role,
            responsibilities=list(juso.responsibilities),
            greeting=juso.greeting,
        )
