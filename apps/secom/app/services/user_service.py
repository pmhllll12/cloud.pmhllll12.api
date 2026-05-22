"""secom 사용자 비즈니스 로직."""

from __future__ import annotations

import logging
import re

import bcrypt

from secom.app.models.user_model import User
from secom.app.repositories.user_repository import UserRepository
from secom.schemas.user_schemas import UserSchemas

logger = logging.getLogger(__name__)

SEED_ADMIN_EMAIL = "pmhllll12@gmail.com"
SEED_USER_EMAIL = "user@pmhllll12.local"
SEED_PASSWORD = "12#$alsgh"
SEED_PASSWORD_CONFIRM = "12#$alsgh"
_PHONE_RE = re.compile(r"^01[0-9][0-9]{7,8}$")


def _hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def _normalize_phone(phone: str) -> str:
    return re.sub(r"\D", "", phone.strip())


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def save_user(self, user_schema: UserSchemas) -> User:
        logger.info(
            "[UserService] save_user 레이어 진입 — user_id=%s",
            user_schema.user_id,
        )
        if user_schema.password != user_schema.password_confirm:
            raise ValueError("password 와 password_confirm 이 일치하지 않습니다.")

        user_id_key = user_schema.user_id.strip()
        email_key = user_schema.email.strip()
        phone_key = _normalize_phone(user_schema.phone)
        if not _PHONE_RE.match(phone_key):
            raise ValueError("휴대전화 번호 형식이 올바르지 않습니다. (예: 01012345678)")

        existing_uid = await self._repository.get_by_user_id(user_id_key)
        if existing_uid is not None:
            raise ValueError(
                f"아이디 '{user_id_key}' 는 이미 사용 중입니다. 다른 아이디를 입력하세요."
            )
        existing_email = await self._repository.get_by_email(email_key)
        if existing_email is not None:
            raise ValueError(
                f"이메일 '{email_key}' 는 이미 등록되어 있습니다. 로그인하거나 다른 이메일을 사용하세요."
            )

        entity = User(
            user_id=user_id_key,
            email=email_key,
            nickname=user_schema.nickname.strip(),
            phone=phone_key,
            password_hash=_hash_password(user_schema.password),
            role=user_schema.role.strip().lower(),
        )
        saved = await self._repository.save_user(entity)
        logger.info(
            "[UserService] save_user 레이어 완료 — user_id=%s",
            saved.user_id,
        )
        return saved
