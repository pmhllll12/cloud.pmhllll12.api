from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository

class LoweBoatInteractor(LoweBoatUseCase):

    def __init__(self, repository: LoweBoatRepository):
        self.repository = repository

    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
            '''로우 구명정의 자기소개 인터렉트'''
        query = LoweBoatQuery(
            id=schema.id,
            name=schema.name
        )
        return await self.repository.introduce_myself(query)
    
    async def upload_titanic_file(self, schema: list[LoweBoatSchema]) -> None:
        '''로우 구명정의 타이타닉 파일업로드 인터렉트'''
        for item in schema:
            query = LoweBoatQuery(
                id=item.id,
                name=item.name
            )
            await self.repository.upload_titanic_file(query)