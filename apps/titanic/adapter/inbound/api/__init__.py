"""HTTP API adapters — Titanic V1 라우터를 한 데 묶어 노출."""

from __future__ import annotations

from fastapi import APIRouter

from titanic.adapter.inbound.api.V1.crew_andrews_architect_router import (
    andrews_architect_router as crew_andrews_architect_router,
)
from titanic.adapter.inbound.api.V1.crew_hartley_violin_router import (
    hartley_violin_router as crew_hartley_violin_router,
)
from titanic.adapter.inbound.api.V1.crew_james_director_router import (
    james_director_router as crew_james_director_router,
)
from titanic.adapter.inbound.api.V1.crew_smith_captin_router import (
    smith_captain_router as crew_smith_captin_router,
)
from titanic.adapter.inbound.api.V1.crew_walter_roaster_router import (
    walter_roaster_router as crew_walter_roaster_router,
)
from titanic.adapter.inbound.api.V1.passenger_cal_tester_router import (
    cal_tester_router as passenger_cal_tester_router,
)
from titanic.adapter.inbound.api.V1.passenger_isidor_couple_router import (
    isidor_couple_router as passenger_isidor_couple_router,
)
from titanic.adapter.inbound.api.V1.passenger_jack_trainer_router import (
    jack_trainer_router as passenger_jack_trainer_router,
)
from titanic.adapter.inbound.api.V1.passenger_rose_model_router import (
    rose_model_router as passenger_rose_model_router,
)
from titanic.adapter.inbound.api.V1.passenger_ruth_validation_router import (
    ruth_validation_router as passenger_ruth_validation_router,
)

# 레거시 별칭 (기존 `james_router` import 호환)
james_router = crew_james_director_router

titanic_router = APIRouter(prefix="/titanic", tags=["titanic"])
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

__all__ = ["titanic_router", "james_router"]
