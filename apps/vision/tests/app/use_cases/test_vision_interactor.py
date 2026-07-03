from __future__ import annotations

import asyncio
from datetime import datetime

from vision.app.dtos.vision_dto import AnalyzedImageLog, AnalyzeImageCommand
from vision.app.ports.output.image_captioning_port import ImageCaptioningPort
from vision.app.ports.output.vision_port import VisionPort
from vision.app.use_cases.vision_interactor import VisionInteractor


class _StubCaptioner(ImageCaptioningPort):
    def __init__(self, caption: str = "고양이 사진", tags: list[str] | None = None) -> None:
        self.caption_text = caption
        self.tags_list = tags if tags is not None else ["고양이", "동물"]
        self.calls = 0

    async def caption(self, content: bytes, mime_type: str) -> tuple[str, list[str]]:
        self.calls += 1
        return self.caption_text, self.tags_list


class _StubRepository(VisionPort):
    def __init__(self) -> None:
        self.saved: list[dict] = []

    async def save(
        self,
        filename: str,
        caption: str,
        tags: list[str],
        analyzed_at: datetime,
    ) -> None:
        self.saved.append(
            {
                "filename": filename,
                "caption": caption,
                "tags": tags,
                "analyzed_at": analyzed_at,
            }
        )

    async def list_recent(self, limit: int = 100) -> list[AnalyzedImageLog]:
        return [
            AnalyzedImageLog(
                analyzed_at=row["analyzed_at"].isoformat(),
                filename=row["filename"],
                caption=row["caption"],
                tags=row["tags"],
            )
            for row in self.saved
        ]


def _make_interactor() -> tuple[VisionInteractor, _StubRepository, _StubCaptioner]:
    repository = _StubRepository()
    captioner = _StubCaptioner()
    interactor = VisionInteractor(repository=repository, captioner=captioner)
    return interactor, repository, captioner


def test_analyze_saves_caption_and_tags():
    async def _run():
        interactor, repository, _ = _make_interactor()
        result = await interactor.analyze(
            AnalyzeImageCommand(filename="cat.jpg", content=b"fake-bytes", mime_type="image/jpeg")
        )
        return repository, result

    repository, result = asyncio.run(_run())
    assert result.ok is True
    assert result.caption == "고양이 사진"
    assert len(repository.saved) == 1
    assert repository.saved[0]["filename"] == "cat.jpg"
    assert repository.saved[0]["tags"] == ["고양이", "동물"]


def test_get_logs_returns_saved_entries():
    async def _run():
        interactor, *_ = _make_interactor()
        await interactor.analyze(
            AnalyzeImageCommand(filename="dog.png", content=b"fake-bytes", mime_type="image/png")
        )
        return await interactor.get_logs()

    logs = asyncio.run(_run())
    assert len(logs) == 1
    assert logs[0].filename == "dog.png"


def test_analyze_calls_captioner_once():
    async def _run():
        interactor, _, captioner = _make_interactor()
        await interactor.analyze(
            AnalyzeImageCommand(filename="cat.jpg", content=b"fake-bytes", mime_type="image/jpeg")
        )
        return captioner

    captioner = asyncio.run(_run())
    assert captioner.calls == 1
