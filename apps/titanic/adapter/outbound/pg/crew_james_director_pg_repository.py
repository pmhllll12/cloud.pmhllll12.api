"""James — Neon PostgreSQL (`crew_james_director` 유스케이스)."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine as neon_engine
from titanic.adapter.outbound.orm.crew_james_booking_orm import JamesBooking
from titanic.adapter.outbound.orm.crew_james_person_orm import JamesPerson
from titanic.app.dtos.crew_james_director_dto import BookingCommand, PersonCommand
from titanic.app.ports.output.crew_james_director_repository import JamesRepository

logger = logging.getLogger(__name__)


class JamesDirectorPgRepository(JamesRepository):
    def __init__(self, session: Any) -> None:
        self.session = session

    async def receive_uploaded_records(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        if self.session is None:
            logger.warning("[제임스 레포지토리] 세션 없음 — DB 적재 생략, 상위 5행만 로그")
            for person in person_commands[:5]:
                logger.info("%s", person)
            for booking in booking_commands[:5]:
                logger.info("%s", booking)
            return len(person_commands)

        session: AsyncSession = self.session

        try:
            if neon_engine is not None:
                async with neon_engine.begin() as conn:
                    await conn.run_sync(
                        lambda sync_conn: Base.metadata.create_all(
                            sync_conn,
                            tables=[JamesPerson.__table__, JamesBooking.__table__],
                            checkfirst=True,
                        ),
                    )

            await session.execute(delete(JamesBooking))
            await session.execute(delete(JamesPerson))
            await session.flush()

            for p in person_commands:
                session.add(
                    JamesPerson(
                        passenger_id=p.passenger_id,
                        booking_id=p.booking_id,
                        embarked_code=p.embarked_code,
                        name=p.name,
                        gender=p.gender,
                        age=p.age,
                        sib_sp=p.sib_sp,
                        parch=p.parch,
                        survived=p.survived,
                    )
                )
            for b in booking_commands:
                session.add(
                    JamesBooking(
                        booking_id=b.booking_id,
                        pclass=b.pclass,
                        ticket=b.ticket,
                        fare=b.fare,
                        cabin=b.cabin,
                        embarked_code=b.embarked_code,
                        port_name=b.port_name,
                    )
                )

            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            logger.exception("[제임스 레포지토리] Neon 적재 중 SQLAlchemy 오류")
            raise

        logger.info(
            "[제임스 레포지토리] Neon 적재 완료 — persons=%s bookings=%s",
            len(person_commands),
            len(booking_commands),
        )
        return len(person_commands)
