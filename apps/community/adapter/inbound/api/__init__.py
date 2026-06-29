from fastapi import APIRouter

from community.adapter.inbound.api.v1.email_router import email_router

community_router = APIRouter(prefix="/api/community")
community_router.include_router(email_router)
