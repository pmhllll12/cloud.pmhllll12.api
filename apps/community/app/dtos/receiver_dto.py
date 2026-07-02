from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReceiveEmailCommand:
    subject: str
    from_: str | None
    to: str | None
    body: str | None


@dataclass(frozen=True)
class ReceiveEmailResult:
    ok: bool
    message: str


@dataclass(frozen=True)
class ReceivedEmailLog:
    received_at: str
    subject: str
    from_: str | None
    to: str | None
    body: str | None
