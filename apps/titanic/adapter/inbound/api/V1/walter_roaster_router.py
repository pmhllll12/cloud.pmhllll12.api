"""Walter — 로스터(독서/열람) 스텁 (`/titanic/walter-roaster`)."""

from __future__ import annotations

from fastapi import APIRouter

walter_roaster_router = APIRouter(
    prefix="/titanic/walter-roaster",
    tags=["walter-roaster"],
)


@walter_roaster_router.post("/roast")
async def get_roast() -> dict[str, object]:
    """열람·요약 스텁 엔드포인트."""
    return {
        "ok": True,
        "name": "Walter",
        "item": "reader / roster stub",
        "endpoint": "/roast",
        "note": "stub — `walter_reader` 등 앱 로직과 연동 시 확장",
    }
