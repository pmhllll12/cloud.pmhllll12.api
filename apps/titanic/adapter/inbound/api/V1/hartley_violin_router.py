"""Wallace Hartley — 바이올린 스텁 (`/titanic/hartley-violin`)."""

from __future__ import annotations

from fastapi import APIRouter

hartley_violin_router = APIRouter(
    prefix="/hartley-violin",
    tags=["hartley-violin"],
)


@hartley_violin_router.post("/violin")
async def get_violin() -> dict[str, object]:
    """바이올린·연주 목록 플레이스홀더."""
    return {
        "ok": True,
        "name": "Wallace Hartley",
        "item": "violin",
        "endpoint": "/violin",
        "note": "stub — 추후 세트리스트·오디오 메타 연동",
    }
