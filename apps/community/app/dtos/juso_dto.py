from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JusoQuery:
    id: int
    name: str


@dataclass(frozen=True)
class JusoResult:
    id: int
    name: str
    role: str
    responsibilities: tuple[str, ...]
    greeting: str
