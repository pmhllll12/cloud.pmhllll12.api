from __future__ import annotations

from pydantic import BaseModel


class JusoSchema(BaseModel):
    id: int
    name: str


class JusoResponse(BaseModel):
    id: int
    name: str
    role: str
    responsibilities: list[str]
    greeting: str
