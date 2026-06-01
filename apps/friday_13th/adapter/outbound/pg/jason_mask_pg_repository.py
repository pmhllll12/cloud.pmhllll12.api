from sqlalchemy.ext.asyncio import AsyncSession
from friday_13th.app.ports.output.jason_mask_repository import JasonMaskRepository

class JasonMaskPgRepository(JasonMaskRepository):
    def __init__(self, session: AsyncSession):


    