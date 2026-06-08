"""Walter Roaster 의존성 조립소 (DIP). `schemas/crew_walter_roaster_schemas` 흐름."""

from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.adapter.outbound.pg.crew_walter_roaster_pg_repository import WalterRoasterPgRepository
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUsecase
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository
from titanic.app.use_cases.crew_walter_roaster_interactor import WalterRoasterInteractor


def get_crew_walter_roaster_use_case(
    db: AsyncSession = Depends(get_db),
) -> WalterRoasterUsecase:
    repository: WalterRoasterRepository = WalterRoasterPgRepository(session=db)
    return WalterRoasterInteractor(repository=repository)


get_walter_roaster_use_case = get_crew_walter_roaster_use_case
