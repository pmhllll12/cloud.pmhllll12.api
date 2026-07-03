from fastapi import APIRouter
from vision.adapter.inbound.api.v1.vision_router import image_analysis_router

vision_router = APIRouter(prefix="/api/vision")
vision_router.include_router(image_analysis_router)
