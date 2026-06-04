"""Alembic — Neon `DATABASE_URL`, 루트 `database.Base` + James ORM 메타데이터."""

from __future__ import annotations

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine, pool

# `titanic` 은 `backend/apps/` 아래, `database` 는 `backend/` 루트 — 둘 다 path 에 필요
_ROOT = Path(__file__).resolve().parents[1]
_APPS = _ROOT / "apps"
for _dir in (_APPS, _ROOT):
    _p = str(_dir)
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dotenv import load_dotenv

load_dotenv(_APPS / ".env")
load_dotenv(_ROOT / ".env")

from database import Base  # noqa: E402
from database import alembic_database_url  # noqa: E402

# 메타데이터에 ORM 테이블 등록
from titanic.adapter.outbound.orm import booking_orm  # noqa: E402, F401
from titanic.adapter.outbound.orm import person_orm  # noqa: E402, F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    url = alembic_database_url()
    config.set_main_option("sqlalchemy.url", url)
    return url


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = get_url()
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
