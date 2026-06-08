"""플레이스홀더 라우터 — `schemas/passenger_ruth_survivor_schemas`."""

from fastapi import APIRouter

passenger_ruth_survivor_router = APIRouter(prefix="/ruth", tags=["ruth"])
ruth_corset_router = passenger_ruth_survivor_router
