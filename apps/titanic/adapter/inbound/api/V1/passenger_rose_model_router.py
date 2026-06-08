"""플레이스홀더 라우터 — `schemas/passenger_rose_model_schemas`."""

from fastapi import APIRouter

passenger_rose_model_router = APIRouter(prefix="/rose", tags=["rose"])
rose_diamond_router = passenger_rose_model_router
