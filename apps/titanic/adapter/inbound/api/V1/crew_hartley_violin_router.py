"""플레이스홀더 라우터 — `schemas/crew_hartley_violin_schemas`."""

from fastapi import APIRouter

crew_hartley_violin_router = APIRouter(prefix="/hartley", tags=["hartley"])
hartley_violin_router = crew_hartley_violin_router
