from __future__ import annotations

from pydantic import BaseModel


class TelegramSchema(BaseModel):
    id: int
    name: str


class TelegramResponse(BaseModel):
    id: int
    name: str
    role: str
    channels: list[str]
    greeting: str
