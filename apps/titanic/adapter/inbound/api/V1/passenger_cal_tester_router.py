"""플레이스홀더 라우터 — `schemas/passenger_cal_tester_schemas`."""

from fastapi import APIRouter

passenger_cal_tester_router = APIRouter(prefix="/cal", tags=["cal"])
cal_pistol_router = passenger_cal_tester_router
