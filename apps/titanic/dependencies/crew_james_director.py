"""James Director 의존성 조립소 (DIP). `schemas/crew_james_director_schema` 흐름."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_optional

if TYPE_CHECKING:
    from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase


def get_crew_james_director_use_case(
    db: AsyncSession | None = Depends(get_db_optional),
) -> JamesDirectorUseCase:
    from titanic.adapter.outbound.pg.crew_james_director_pg_repository import JamesDirectorPgRepository
    from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
    from titanic.app.ports.output.crew_james_director_repository import JamesRepository
    from titanic.app.use_cases.crew_james_director_interactor import JamesDirectorInteractor

    repository: JamesRepository = JamesDirectorPgRepository(session=db)
    return JamesDirectorInteractor(repository=repository)


# 하위 호환 별칭
get_james_director_use_case = get_crew_james_director_use_case
