from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery


class LoweBoatRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: LoweBoatQuery):
        """로우 구명정 레포지토리 추상 메소드"""
        raise NotImplementedError
