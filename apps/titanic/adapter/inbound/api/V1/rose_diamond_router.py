"""Rose DeWitt Bukater — 다이아몬드(하트 오브 오션) 스텁 (`/titanic/rose-diamond`)."""

from __future__ import annotations

from fastapi import APIRouter

rose_diamond_router = APIRouter(
    prefix="/titanic/rose-diamond",
    tags=["rose-diamond"],
)


@rose_diamond_router.post("/diamond")
async def get_diamond() -> dict[str, object]:
    """목걸이·보석 메타 플레이스홀더."""
    return {
        "ok": True,
        "name": "Rose DeWitt Bukater",
        "item": "Heart of the Ocean (stub)",
        "endpoint": "/diamond",
        "note": "stub — 추후 인벤토리·씬 연동",
    }
