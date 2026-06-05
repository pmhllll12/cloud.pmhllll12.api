"""James CSV 업로드 유스케이스."""

from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.james_director_schema import JamesDirectorRecordsSchema
from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_director_repository import JamesRepository

logger = logging.getLogger(__name__)

_PORT: dict[str, str] = {"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"}


def _embarked_code(raw: str | None) -> str:
    if raw is None or not str(raw).strip():
        return ""
    return str(raw).strip().upper()[:1]


class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def upload_titanic_file(self, schema: JamesDirectorRecordsSchema) -> None:
        logger.info("[제임스 유스케이스] 스키마 상위 5개 레코드:")
        for record in schema.rows[:5]:
            logger.info("%s", record)

        person_commands: list[PersonCommand] = []
        booking_commands: list[BookingCommand] = []

        for record in schema.rows:
            bid = str(record.passenger_id)
            ec = _embarked_code(record.embarked)
            person_commands.append(
                PersonCommand(
                    passenger_id=str(record.passenger_id),
                    booking_id=bid,
                    embarked_code=ec,
                    name=record.name,
                    gender=record.gender,
                    age="" if record.age is None else str(record.age),
                    sib_sp=str(record.sib_sp),
                    parch=str(record.parch),
                    survived=str(record.survived),
                )
            )
            booking_commands.append(
                BookingCommand(
                    booking_id=bid,
                    pclass=str(record.pclass),
                    ticket=record.ticket,
                    fare=str(record.fare),
                    cabin=record.cabin or "",
                    embarked_code=ec,
                    port_name=_PORT.get(ec, ""),
                )
            )

        await self._repository.upload_titanic_file(person_commands, booking_commands)
