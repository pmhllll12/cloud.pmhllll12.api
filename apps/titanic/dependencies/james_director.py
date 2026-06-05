"""James Director 의존성 조립소 (DIP 팩토리).

DIP:
  - 입력 어댑터(라우터)는 `JamesDirectorPgRepository` 같은 구현체를 직접 알지 않는다.
  - 이 모듈만 `JamesRepository` 구현체를 만들어 `JamesDirectorInteractor`에 주입한다.
  - 반환 타입은 입력 포트(`JamesDirectorUseCase`)다.
  - DB 세션은 `get_db_optional` 로 주입한다 (Neon 미설정 시 `None`).

  상단에서 `titanic.app.ports`·어댑터를 import 하지 않는다.
  `james_director_use_case` 가 스키마를 통해 `api` 패키지를 끌어오면서
  `james_director_router` 와 순환 import 가 나기 때문이다. 조립은 팩토리 호출 시점에만 한다.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_optional

if TYPE_CHECKING:
    from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase


def get_james_director_use_case(
    db: AsyncSession | None = Depends(get_db),
) -> JamesDirectorUseCase:
    from titanic.adapter.outbound.pg.james_director_pg_repository import JamesDirectorPgRepository
    from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
    from titanic.app.ports.output.james_director_repository import JamesRepository
    from titanic.app.use_cases.james_director_interactor import JamesDirectorInteractor

    repository: JamesRepository = JamesDirectorPgRepository(session=db)
    return JamesDirectorInteractor(repository=repository)
