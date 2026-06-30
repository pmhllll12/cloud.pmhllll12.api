from __future__ import annotations

from abc import ABC, abstractmethod

from community.app.dtos.juso_dto import JusoContactRecord


class JusoContactPort(ABC):
    @abstractmethod
    async def save_contacts(self, records: list[JusoContactRecord]) -> int:
        raise NotImplementedError
