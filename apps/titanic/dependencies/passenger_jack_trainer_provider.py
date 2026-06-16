from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.adapter.outbound.pg.passenger_jack_trainer_pg_repository import JackTrainPgRepository
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainRepository
from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor


def get_jack_trainer_repository(
    db: AsyncSession = Depends(get_db),
) -> JackTrainRepository:
    return JackTrainPgRepository(session=db)


def get_jack_train_use_case(
    repository: JackTrainRepository = Depends(get_jack_trainer_repository),
) -> JackTrainerUseCase:
    return JackTrainerInteractor(repository=repository)



