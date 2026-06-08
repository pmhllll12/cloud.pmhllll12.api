"""플레이스홀더 라우터 — `schemas/passenger_jack_trainer_schemas`."""

from fastapi import APIRouter

passenger_jack_trainer_router = APIRouter(prefix="/jack", tags=["jack"])
jack_sketch_router = passenger_jack_trainer_router
