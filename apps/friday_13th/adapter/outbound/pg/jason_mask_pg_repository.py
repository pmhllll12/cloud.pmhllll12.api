from friday_13th.app.ports.output.jason_mask_repository import JasonMaskRepository
from sqlalchemy.ext.asyncio import AsyncSession


class JasonMaskPgRepository(JasonMaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
