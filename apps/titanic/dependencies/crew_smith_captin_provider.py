from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.adapter.outbound.pg.crew_smith_captin_pg_repository import SmithCaptainPgRepository
from titanic.app.ports.input.crew_smith_captin_use_case import SmithCaptainUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captin_repository import SmithCaptainRepository
from titanic.app.use_cases.crew_smith_captin_interactor import SmithCaptainInteractor
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_train_use_case
from titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case


def get_smith_captain_use_case(
    db: AsyncSession = Depends(get_db),
    jack: JackTrainerUseCase = Depends(get_jack_train_use_case),
    rose: RoseModelUseCase = Depends(get_rose_model_use_case),
) -> SmithCaptainUseCase:
    repository: SmithCaptainRepository = SmithCaptainPgRepository(session=db)
    return SmithCaptainInteractor(repository=repository, jack=jack, rose=rose)
