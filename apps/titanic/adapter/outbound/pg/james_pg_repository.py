"""James 업로드 PostgreSQL 저장소 — 아웃바운드 데이터를 Neon DB로 전송."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import delete, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.james_passenger_orm import JamesPassenger
from titanic.app.ports.output.james_repository import JamesRepositoryPort
from titanic.app.titanic_csv_parser import API_COLUMNS

logger = logging.getLogger(__name__)


class JamesPgRepository(JamesRepositoryPort):
    """`JamesCommand`에서 넘어온 행을 ORM으로 변환한 뒤 `commit()` 으로 Neon에 저장."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_upload(
        self,
        *,
        filename: str,
        columns: list[str],
        rows: list[dict[str, Any]],
    ) -> int:
        if not rows:
            return 0

        logger.info(
            "[JamesPgRepository] Neon DB 저장 시작 — filename=%s rows=%s",
            filename,
            len(rows),
        )

        try:
            await self._session.execute(delete(JamesPassenger))
            self._session.add_all(
                JamesPassenger.from_record(filename, row) for row in rows
            )
            # commit() 시점에 Neon PostgreSQL 로 실제 전송·저장
            await self._session.commit()
        except SQLAlchemyError as exc:
            await self._session.rollback()
            logger.exception("Neon DB 전송 실패: %s", exc)
            raise ValueError(f"Neon DB 저장에 실패했습니다: {exc}") from exc

        logger.info(
            "[JamesPgRepository] Neon DB commit 완료 — titanic_james_passengers 에 %s행 저장됨 (filename=%s)",
            len(rows),
            filename,
        )
        return len(rows)

    async def fetch_page(
        self,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        count_result = await self._session.execute(
            select(func.count()).select_from(JamesPassenger)
        )
        total = int(count_result.scalar_one())

        offset = (page - 1) * page_size
        result = await self._session.execute(
            select(JamesPassenger)
            .order_by(JamesPassenger.passenger_id)
            .offset(offset)
            .limit(page_size)
        )
        rows = [p.to_api_row() for p in result.scalars().all()]
        logger.info(
            "[JamesPgRepository] 승객 목록 조회 — page=%s size=%s total=%s",
            page,
            page_size,
            total,
        )
        return rows, total

    @staticmethod
    def api_columns() -> list[str]:
        return list(API_COLUMNS)
