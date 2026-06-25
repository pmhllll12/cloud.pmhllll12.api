from friday_13th.app.ports.output.pamela_cook_repository import PamelaCookRepository
from sqlalchemy.ext.asyncio import AsyncSession


class PamelaCookPgRepository(PamelaCookRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def signup(self, username: str, password: str) -> bool:
        pass