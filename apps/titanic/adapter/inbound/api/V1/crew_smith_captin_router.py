"""플레이스홀더 라우터 — `schemas/crew_smith_captin_schemas`."""

from fastapi import APIRouter

crew_smith_captin_router = APIRouter(prefix="/smith", tags=["smith"])
smith_captin_router = crew_smith_captin_router
