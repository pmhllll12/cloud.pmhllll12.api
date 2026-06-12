from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.adapter.outbound.pg.passenger_jack_trainer_pg_repository import JackTrainPgRepository
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainRepository
from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor


def get_jack_trainer(
        db: AsyncSession = Depends(get_db)
) -> JackTrainerUseCase:
    repository: JackTrainRepository = JackTrainPgRepository(session=db)
    return JackTrainerInteractor(repository=repository)


# 라우터 등에서 예전 이름으로 import 하는 경우 호환
get_jack_train_use_case = get_jack_trainer
