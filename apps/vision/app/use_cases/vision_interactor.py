from __future__ import annotations

import logging
from datetime import datetime

from vision.app.dtos.vision_dto import (
    AnalyzedImageLog,
    AnalyzeImageCommand,
    AnalyzeImageResult,
)
from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.app.ports.output.image_captioning_port import ImageCaptioningPort
from vision.app.ports.output.vision_port import VisionPort
from vision.domain.analyzed_image import AnalyzedImage

logger = logging.getLogger(__name__)


class VisionInteractor(VisionUseCase):
    def __init__(self, repository: VisionPort, captioner: ImageCaptioningPort) -> None:
        self.repository = repository
        self.captioner = captioner

    async def analyze(self, command: AnalyzeImageCommand) -> AnalyzeImageResult:
        caption, tags = await self.captioner.caption(command.content, command.mime_type)

        image = AnalyzedImage(
            filename=command.filename,
            caption=caption,
            tags=tags,
            analyzed_at=datetime.now(),
        )
        await self.repository.save(
            filename=image.filename,
            caption=image.caption,
            tags=image.tags,
            analyzed_at=image.analyzed_at,
        )
        logger.info(
            "[VisionInteractor] analyze filename=%r caption=%r", image.filename, image.caption
        )
        return AnalyzeImageResult(ok=True, caption=caption, tags=tags)

    async def get_logs(self) -> list[AnalyzedImageLog]:
        return await self.repository.list_recent()
