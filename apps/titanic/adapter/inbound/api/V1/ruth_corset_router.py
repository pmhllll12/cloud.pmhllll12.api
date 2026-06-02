"""Ruth DeWitt Bukater — 코르셋·복장 스텁 (`/titanic/ruth-corset`)."""

from __future__ import annotations

from fastapi import APIRouter

ruth_corset_router = APIRouter(
    prefix="/ruth-corset",
    tags=["ruth-corset"],
)


@ruth_corset_router.post("/corset")
async def get_corset() -> dict[str, object]:
    """의상·에티켓 메타 플레이스홀더."""
    return {
        "ok": True,
        "name": "Ruth DeWitt Bukater",
        "item": "corset / dress code",
        "endpoint": "/corset",
        "note": "stub — 추후 의상·사회 규범 메타 연동",
    }
