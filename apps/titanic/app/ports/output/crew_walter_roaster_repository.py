from abc import ABC, abstractmethod

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse


class WalterRoasterRepository(ABC):
    """월터의 승객 명단 관리 저장소."""

    @abstractmethod
    def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        raise NotImplementedError