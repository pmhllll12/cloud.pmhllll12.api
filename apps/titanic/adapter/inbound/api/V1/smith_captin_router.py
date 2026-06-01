"""Edward Smith — 선장 스텁 (`/titanic/smith-captin`). 파일명 `captin` 유지."""

from __future__ import annotations

from fastapi import APIRouter

smith_captin_router = APIRouter(
    prefix="/titanic/smith-captin",
    tags=["smith-captin"],
)


@smith_captin_router.post("/captain")
async def get_captain() -> dict[str, object]:
    """브리지·항해 명령 스텁."""
    return {
        "ok": True,
        "name": "Edward Smith",
        "role": "captain",
        "endpoint": "/captain",
        "note": "stub — 추후 항해 로그·명령 메타 연동",
    }
