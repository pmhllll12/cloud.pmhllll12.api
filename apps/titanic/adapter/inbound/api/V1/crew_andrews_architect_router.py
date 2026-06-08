"""플레이스홀더 라우터 — `schemas/crew_andrews_architect_schemas`."""

from fastapi import APIRouter

crew_andrews_architect_router = APIRouter(prefix="/andrews", tags=["andrews"])
andrews_blueprint_router = crew_andrews_architect_router
