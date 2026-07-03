from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalyzeImageCommand:
    filename: str
    content: bytes
    mime_type: str


@dataclass(frozen=True)
class AnalyzeImageResult:
    ok: bool
    caption: str
    tags: list[str]
    message: str = "analyzed"


@dataclass(frozen=True)
class AnalyzedImageLog:
    analyzed_at: str
    filename: str
    caption: str
    tags: list[str]
