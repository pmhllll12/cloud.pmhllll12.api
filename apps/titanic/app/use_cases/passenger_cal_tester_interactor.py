from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schemas import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_repository import CalTestRepository


class CalTesterInteractor(CalTesterUseCase):
    def __init__(self, repository: CalTestRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        query = CalTesterQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
