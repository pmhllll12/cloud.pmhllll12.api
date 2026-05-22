"""secom 사용자 영속화."""

from __future__ import annotations

import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.models.user_model import User

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_user(self, user: User) -> User:
        logger.info(
            "[UserRepository] save_user 레이어 진입 — user_id=%s",
            user.user_id,
        )
        self._session.add(user)
        await self._session.flush()
        await self._session.commit()
        await self._session.refresh(user)
        logger.info(
            "[UserRepository] save_user 레이어 완료 — Neon 반영 id=%s user_id=%s",
            user.id,
            user.user_id,
        )
        return user

    async def get_by_user_id(self, user_id: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def count_all(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(User))
        return int(result.scalar_one())

    async def list_all(self) -> list[User]:
        result = await self._session.execute(select(User).order_by(User.id))
        return list(result.scalars().all())
