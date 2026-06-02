"""Isidor Straus — 선실(침대) 스텁 (`/titanic/isidor-bed`)."""

from __future__ import annotations

from fastapi import APIRouter

isidor_bed_router = APIRouter(prefix="/isidor-bed", tags=["isidor-bed"])


@isidor_bed_router.post("/bed")
async def get_bed() -> dict[str, object]:
    """선실·숙소 메타 플레이스홀더."""
    return {
        "ok": True,
        "name": "Isidor Straus",
        "item": "cabin",
        "endpoint": "/bed",
        "note": "stub — 추후 객실 배정 메타 연동",
    }
