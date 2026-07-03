from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from vision.app.dtos.vision_dto import AnalyzedImageLog


class VisionPort(ABC):
    @abstractmethod
    async def save(
        self,
        filename: str,
        caption: str,
        tags: list[str],
        analyzed_at: datetime,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_recent(self, limit: int = 100) -> list[AnalyzedImageLog]:
        raise NotImplementedError
