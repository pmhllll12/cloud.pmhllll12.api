from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


class MollyScalerPgRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: MollyScalerQuery) -> MollyScalerResponse:
        '''월터의 자기 소개 레포지토리 구현 메소드'''
        logger.info(f"[MollyScalerPgRepository] introduce_myself 진입 | request_data={query}")
        response: MollyScalerResponse = MollyScalerResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response
        