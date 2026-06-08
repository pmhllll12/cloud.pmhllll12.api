"""HTTP API adapters — Titanic V1 라우터를 한 데 묶어 노출."""

from __future__ import annotations

from fastapi import APIRouter

from titanic.adapter.inbound.api.V1.crew_andrews_architect_router import crew_andrews_architect_router
from titanic.adapter.inbound.api.V1.crew_hartley_violin_router import crew_hartley_violin_router
from titanic.adapter.inbound.api.V1.crew_james_director_router import (
    crew_james_director_router,
    james_router,
    list_passengers_titanic_root,
)
from titanic.adapter.inbound.api.V1.crew_smith_captin_router import crew_smith_captin_router
from titanic.adapter.inbound.api.V1.crew_walter_roaster_router import crew_walter_roaster_router
from titanic.adapter.inbound.api.V1.passenger_cal_tester_router import passenger_cal_tester_router
from titanic.adapter.inbound.api.V1.passenger_isidor_couple_router import passenger_isidor_couple_router
from titanic.adapter.inbound.api.V1.passenger_jack_trainer_router import passenger_jack_trainer_router
from titanic.adapter.inbound.api.V1.passenger_rose_model_router import passenger_rose_model_router
from titanic.adapter.inbound.api.V1.passenger_ruth_validation_router import passenger_ruth_validation_router
from titanic.adapter.inbound.api.schemas.crew_james_director_schema import JamesDirectorPassengersListResponse

titanic_router = APIRouter(prefix="/titanic", tags=["titanic"])
# 수업용 UI 등에서 `/titanic/passengers` 로 호출하는 경우를 위해 루트 별칭
titanic_router.add_api_route(
    "/passengers",
    list_passengers_titanic_root,
    methods=["GET"],
    response_model=JamesDirectorPassengersListResponse,
)
titanic_router.include_router(crew_james_director_router)
titanic_router.include_router(passenger_rose_model_router)
titanic_router.include_router(crew_walter_roaster_router)
titanic_router.include_router(crew_andrews_architect_router)
titanic_router.include_router(passenger_cal_tester_router)
titanic_router.include_router(crew_hartley_violin_router)
titanic_router.include_router(passenger_isidor_couple_router)
titanic_router.include_router(passenger_jack_trainer_router)
titanic_router.include_router(passenger_ruth_validation_router)
titanic_router.include_router(crew_smith_captin_router)

# 레거시 별칭 (기존 `james_router` import 호환)
__all__ = ["titanic_router", "james_router"]
