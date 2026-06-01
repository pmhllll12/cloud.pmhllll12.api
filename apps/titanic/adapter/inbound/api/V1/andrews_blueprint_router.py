"""Thomas Andrews — 설계 도면 스텁 (`/titanic/andrews-blueprint`)."""

from __future__ import annotations

from fastapi import APIRouter

andrews_blueprint_router = APIRouter(
    prefix="/titanic/andrews-blueprint",
    tags=["andrews-blueprint"],
)


@andrews_blueprint_router.post("/blueprint")
async def get_blueprint() -> dict[str, object]:
    """블루프린트 메타데이터 플레이스홀더."""
    return {
        "ok": True,
        "name": "Thomas Andrews",
        "role": "naval architect",
        "endpoint": "/blueprint",
        "note": "stub — 추후 도면·스펙 연동",
    }
