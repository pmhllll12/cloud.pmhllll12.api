"""secom DB 테이블 생성 및 초기 시드."""

from __future__ import annotations

import logging

from sqlalchemy import text

from database import AsyncSessionLocal, Base, engine
from secom.app.controllers.user_controller import UserController
from secom.app.models.user_model import User  # noqa: F401 — Base 메타데이터 등록
from secom.app.repositories.user_repository import UserRepository
from secom.schemas.user_schemas import UserSchemas
from secom.app.services.user_service import (
    SEED_ADMIN_EMAIL,
    SEED_PASSWORD,
    SEED_PASSWORD_CONFIRM,
    SEED_USER_EMAIL,
    UserService,
)

logger = logging.getLogger(__name__)


async def _migrate_secom_user_columns(conn) -> None:
    """기존 secom_users 테이블에 프로필 컬럼이 없으면 추가."""
    for stmt in (
        "ALTER TABLE secom_users ADD COLUMN IF NOT EXISTS user_id VARCHAR(64)",
        "ALTER TABLE secom_users ADD COLUMN IF NOT EXISTS nickname VARCHAR(64)",
        "ALTER TABLE secom_users ADD COLUMN IF NOT EXISTS phone VARCHAR(32)",
    ):
        await conn.execute(text(stmt))
    await conn.execute(
        text(
            "CREATE UNIQUE INDEX IF NOT EXISTS ix_secom_users_user_id "
            "ON secom_users (user_id) WHERE user_id IS NOT NULL"
        )
    )


async def init_secom_db() -> None:
    """DATABASE_URL 이 있을 때만 `secom_users` 테이블 생성 후 시드."""
    if engine is None or AsyncSessionLocal is None:
        logger.info("secom: DB 미사용 — 테이블/시드 생략")
        return

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _migrate_secom_user_columns(conn)

    async with AsyncSessionLocal() as session:
        repo = UserRepository(session)
        if await repo.count_all() > 0:
            logger.info("secom: 기존 사용자 있음 — 시드 생략")
            return

        svc = UserService(repo)
        ctrl = UserController(svc)
        admin_schema = UserSchemas(
            user_id="admin",
            email=SEED_ADMIN_EMAIL,
            nickname="관리자",
            phone="01000000001",
            password=SEED_PASSWORD,
            password_confirm=SEED_PASSWORD_CONFIRM,
            role="admin",
        )
        user_schema = UserSchemas(
            user_id="demo_user",
            email=SEED_USER_EMAIL,
            nickname="데모유저",
            phone="01000000002",
            password=SEED_PASSWORD,
            password_confirm=SEED_PASSWORD_CONFIRM,
            role="user",
        )
        await ctrl.save_user(admin_schema)
        await ctrl.save_user(user_schema)
        logger.info(
            "secom: 초기 사용자 2건 등록 — admin=%s user=%s",
            SEED_ADMIN_EMAIL,
            SEED_USER_EMAIL,
        )
