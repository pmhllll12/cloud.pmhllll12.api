"""플레이스홀더 라우터 — `schemas/passenger_isidor_couple_schemas`."""

from fastapi import APIRouter

passenger_isidor_couple_router = APIRouter(prefix="/isidor", tags=["isidor"])
isidor_bed_router = passenger_isidor_couple_router
