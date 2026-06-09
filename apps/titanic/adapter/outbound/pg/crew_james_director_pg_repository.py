from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import JamesDirectorSchema
from titanic.app.dtos.crew_james_director_dto import (
    BookingCommand,
    JamesDirectorQuery,
    JamesDirectorResponse,
    PassengerCommand,
)
from titanic.app.ports.output.crew_james_director_repository import JamesDirectorRepository

logger = logging.getLogger(__name__)


class JamesDirectorPgRepository(JamesDirectorRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JamesDirectorQuery) -> JamesDirectorResponse:
        logger.info("[JamesDirectorPgRepository] introduce_myself | request_data=%s", query)
        return JamesDirectorResponse(id=query.id, name=query.name)

    async def upload_titanic_file(self, schema: list[JamesDirectorSchema]) -> JamesDirectorResponse:
        """CSV 파싱 결과 행 수만 반환하는 스텁(실제 DB 반영은 receive_uploaded_records 흐름)."""
        logger.info("[JamesDirectorPgRepository] upload_titanic_file | rows=%s", len(schema))
        return JamesDirectorResponse(id=len(schema), name=f"CSV {len(schema)}행 수신")

    async def receive_uploaded_records(
        self,
        person_commands: list[PassengerCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        from titanic.adapter.outbound.orm.booking_orm import BookingOrm
        from titanic.adapter.outbound.orm.passenger_orm import PersonOrm

        person_orms = [
            PersonOrm(
                passenger_id=cmd.passenger_id,
                name=cmd.name,
                gender=cmd.gender,
                age=cmd.age,
                sib_sp=cmd.sib_sp,
                parch=cmd.parch,
                survived=cmd.survived,
            )
            for cmd in person_commands
        ]
        self.session.add_all(person_orms)
        await self.session.flush()

        booking_orms = [
            BookingOrm(
                person_id=person_orm.id,
                pclass=cmd.pclass,
                ticket=cmd.ticket,
                fare=cmd.fare,
                cabin=cmd.cabin,
                embarked=cmd.embarked,
            )
            for person_orm, cmd in zip(person_orms, booking_commands)
        ]
        self.session.add_all(booking_orms)
        await self.session.commit()

        return len(person_orms)