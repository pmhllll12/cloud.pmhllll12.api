"""secom 사용자 HTTP 컨트롤러."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from secom.app.repositories.user_repository import UserRepository
from secom.app.services.user_service import UserService
from secom.schemas.user_schemas import UserSchemas

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/secom/users", tags=["secom-users"])


class UserPublicOut(BaseModel):
    id: int
    user_id: str | None = None
    email: str
    nickname: str | None = None
    phone: str | None = None
    role: str = Field(..., description="admin | user")


class UserController:
    def __init__(self, user_service: UserService) -> None:
        self._user_service = user_service

    async def save_user(self, user_schema: UserSchemas) -> UserPublicOut:
        logger.info(
            "[UserController] save_user 레이어 진입 — user_id=%s",
            user_schema.user_id,
        )
        user = await self._user_service.save_user(user_schema)
        logger.info(
            "[UserController] save_user 레이어 완료 — user_id=%s",
            user.user_id,
        )
        return UserPublicOut(
            id=user.id,
            user_id=user.user_id,
            email=user.email,
            nickname=user.nickname,
            phone=user.phone,
            role=user.role,
        )


@router.get("/", response_model=list[UserPublicOut])
async def list_secom_users(db: AsyncSession = Depends(get_db)) -> list[UserPublicOut]:
    rows = await UserRepository(db).list_all()
    return [
        UserPublicOut(
            id=u.id,
            user_id=u.user_id,
            email=u.email,
            nickname=u.nickname,
            phone=u.phone,
            role=u.role,
        )
        for u in rows
    ]


def register_secom_routes(app) -> None:
    app.include_router(router)
