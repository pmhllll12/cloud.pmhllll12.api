"""James 출력 포트 (`schemas/crew_james_director_schema` 흐름)."""

from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_james_director_dto import BookingCommand, PersonCommand


class JamesRepository(ABC):
    @abstractmethod
    async def receive_uploaded_records(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        ...


__all__ = ["JamesRepository"]
