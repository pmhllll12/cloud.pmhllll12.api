"""Caledon Hockley — 권총 스텁 (`/titanic/cal-pistol`)."""

from __future__ import annotations

from fastapi import APIRouter

cal_pistol_router = APIRouter(prefix="/titanic/cal-pistol", tags=["cal-pistol"])


@cal_pistol_router.post("/pistol")
async def get_pistol() -> dict[str, object]:
    """소품(권총) 메타 플레이스홀더."""
    return {
        "ok": True,
        "name": "Caledon Hockley",
        "item": "pistol",
        "endpoint": "/pistol",
        "note": "stub — 추후 소품·씬 메타 연동",
    }
