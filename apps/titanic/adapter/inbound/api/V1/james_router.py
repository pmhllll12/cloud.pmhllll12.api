"""James — Titanic CSV 업로드 (`/titanic/james`)."""

from __future__ import annotations

import logging
from typing import Annotated

import math

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_session
from titanic.adapter.inbound.api.schemas.james_passengers_response import (
    JamesPassengersPageResponse,
)
from titanic.adapter.inbound.api.schemas.james_response import JamesUploadResponse
from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.app.ports.input.james_use_case import JamesUseCasePort
from titanic.app.use_cases.james_command import JamesCommand

logger = logging.getLogger(__name__)

james_router = APIRouter(prefix="/titanic/james", tags=["james"])


async def get_james_repository(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> JamesPgRepository:
    return JamesPgRepository(session=db)


async def get_james_use_case_port(
    repository: Annotated[JamesPgRepository, Depends(get_james_repository)],
) -> JamesUseCasePort:
    """④ 아웃바운드: Neon 세션을 James PG 레포지토리에 주입."""
    return JamesCommand(repository=repository)


@james_router.post("/upload", response_model=JamesUploadResponse)
async def upload_titanic_csv(
    file: UploadFile = File(...),
    port: Annotated[JamesUseCasePort, Depends(get_james_use_case_port)] = ...,
) -> JamesUploadResponse:
    """CSV 업로드 → 커맨드(Sex→gender) → JamesPgRepository → Neon `commit()`."""
    filename = (file.filename or "").strip()
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    content = await file.read()
    logger.info(
        "[james_router] CSV 수신 — path=/titanic/james/upload filename=%s bytes=%s",
        filename,
        len(content),
    )

    try:
        result = await port.upload_titanic_csv(content, filename)
    except ValueError as exc:
        logger.warning(
            "[james_router] Neon DB 저장 실패 — filename=%s reason=%s",
            filename,
            exc,
        )
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    logger.info(
        "[james_router] Neon DB로 이동 완료 — filename=%s rows=%s columns=%s",
        result.filename,
        result.row_count,
        ", ".join(result.columns),
    )
    return result


@james_router.get("/passengers", response_model=JamesPassengersPageResponse)
async def list_james_passengers(
    repository: Annotated[JamesPgRepository, Depends(get_james_repository)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 50,
) -> JamesPassengersPageResponse:
    """Neon `titanic_james_passengers` 승객 목록 (페이지당 기본 50명)."""
    items, total_count = await repository.fetch_page(page=page, page_size=page_size)
    total_pages = math.ceil(total_count / page_size) if total_count else 0
    return JamesPassengersPageResponse(
        ok=True,
        page=page,
        page_size=page_size,
        total_count=total_count,
        total_pages=total_pages,
        columns=JamesPgRepository.api_columns(),
        items=items,
    )
