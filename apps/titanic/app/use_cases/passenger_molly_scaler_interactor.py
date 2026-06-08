from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema
from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerQuery, MollyScalerResponse
from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from titanic.app.ports.output.passenger_molly_scaler_repository import MollyScalerRepository


class MollyScalerInteractor(MollyScalerUseCase):

    def __init__(self, repository: MollyScalerRepository):
        self.repository = repository

    async def introduce_myself(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        '''몰리 스케일러의 자기소개 인터렉트'''
        query = MollyScalerQuery(
            id=schema.id,
            name=schema.name
        )
        return await self.repository.introduce_myself(query)
    
    async def upload_titanic_file(self, schema: list[MollyScalerSchema]) -> None:
        '''몰리 스케일러의 타이타닉 파일업로드 인터렉트'''
        for item in schema:
            query = MollyScalerQuery(
                id=item.id,
                name=item.name
            )
            await self.repository.upload_titanic_file(query)