from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.walter_roaster_schemas import WalterRoasterSchema

class WalterRoasterUsecase(ABC):


    @abstractmethod
    def introduce_myself(self, schema: WalterRoasterSchema) -> None:
        """월터의 자기소개 메소드."""
        ...

