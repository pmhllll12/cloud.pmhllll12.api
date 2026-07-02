from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from community.app.dtos.receiver_dto import ReceivedEmailLog


class ReceiverPort(ABC):
    @abstractmethod
    async def save(
        self,
        subject: str,
        from_: str | None,
        to: str | None,
        body: str | None,
        received_at: datetime,
        embedding: list[float],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_recent(self, limit: int = 100) -> list[ReceivedEmailLog]:
        raise NotImplementedError
