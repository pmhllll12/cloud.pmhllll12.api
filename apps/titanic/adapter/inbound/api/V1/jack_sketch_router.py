"""Jack Dawson — 스케치 스텁 (`/titanic/jack-sketch`)."""

from __future__ import annotations

from fastapi import APIRouter

jack_sketch_router = APIRouter(prefix="/jack-sketch", tags=["jack-sketch"])


@jack_sketch_router.post("/sketch")
async def get_sketch() -> dict[str, object]:
    """스케치 엔드포인트 플레이스홀더."""
    return {
        "ok": True,
        "name": "Jack Dawson",
        "item": "sketch",
        "endpoint": "/sketch",
        "note": "stub — 추후 스케치 자산 연동",
    }
