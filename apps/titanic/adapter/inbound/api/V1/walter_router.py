"""Walter — Titanic CSV 업로드·조회 (`/titanic/walter`)."""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_session
from titanic.adapter.inbound.api.schemas.walter_response import (
    WalterDataResponse,
    WalterUploadResponse,
)
from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic.app.ports.input.walter_use_case import (
    WalterUseCasePort,
    submit_csv_upload,
    submit_passenger_data_query,
)
from titanic.app.use_cases.walter_query import WalterQuery

logger = logging.getLogger(__name__)

walter_router = APIRouter(prefix="/titanic/walter", tags=["walter"])


async def get_walter_use_case_port(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> WalterUseCasePort:
    logger.info("[walter_router] DI — WalterQuery + WalterPgRepository 생성")
    return WalterQuery(repository=WalterPgRepository(session=db))


@walter_router.post("/upload", response_model=WalterUploadResponse)
async def upload_titanic_csv(
    file: UploadFile = File(...),
    port: Annotated[WalterUseCasePort, Depends(get_walter_use_case_port)] = ...,
) -> WalterUploadResponse:
    """CSV 업로드 → Sex→gender 변환 → Neon `titanic_walter_passengers`."""
    filename = (file.filename or "").strip()
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    content = await file.read()
    logger.info(
        "[walter_router] HTTP POST /titanic/walter/upload — filename=%s bytes=%s → walter_use_case",
        filename,
        len(content),
    )

    try:
        result = await submit_csv_upload(port, content=content, filename=filename)
    except ValueError as exc:
        logger.warning(
            "[walter_router] HTTP 400 — upload 실패 filename=%s reason=%s",
            filename,
            exc,
        )
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    logger.info(
        "[walter_router] HTTP 200 — upload 완료 filename=%s rows=%s",
        result.filename,
        result.row_count,
    )
    return result


@walter_router.get("/data", response_model=WalterDataResponse)
async def read_walter_passenger_data(
    port: Annotated[WalterUseCasePort, Depends(get_walter_use_case_port)] = ...,
) -> WalterDataResponse:
    """저장된 Titanic 데이터를 gender 컬럼 포함해 GET으로 반환합니다."""
    logger.info("[walter_router] HTTP GET /titanic/walter/data → walter_use_case")
    try:
        result = await submit_passenger_data_query(port)
    except ValueError as exc:
        logger.warning("[walter_router] HTTP 400 — fetch 실패 reason=%s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    logger.info(
        "[walter_router] HTTP 200 — fetch 완료 row_count=%s",
        result.row_count,
    )
    return result
