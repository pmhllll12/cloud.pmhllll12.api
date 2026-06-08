from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import JamesDirectorSchema
from titanic.app.dtos.crew_james_director_dto import JamesDirectorQuery, JamesDirectorResponse
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.crew_james_director_repository import JamesDirectorRepository

class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, repository: JamesDirectorRepository):
        self.repository = repository

    async def introduce_myself(self, schema: JamesDirectorSchema) -> JamesDirectorResponse:
        '''제임스 감독의 자기소개 인터렉트'''
        query = JamesDirectorQuery(
            id=schema.id,
            name=schema.name
        )
        return await self.repository.introduce_myself(query)
    
    async def upload_titanic_file(self, schema: list[JamesDirectorSchema]) -> None:
        '''제임스 감독의 타이타닉 파일업로드 인터렉트'''
        for item in schema:
            query = JamesDirectorQuery(
                id=item.id,
                name=item.name
            )
            await self.repository.upload_titanic_file(query)

