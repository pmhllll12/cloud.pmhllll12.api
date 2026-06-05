"""James director — Titanic CSV 업로드 (`/titanic/james`)."""

from __future__ import annotations

import csv
import logging
from io import StringIO
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.exc import SQLAlchemyError

from titanic.adapter.inbound.api.schemas.james_director_schema import (
    JamesDirectorPassengerRow,
    JamesDirectorPassengersListResponse,
    JamesDirectorRecordsSchema,
    JamesDirectorUploadResponse,
)
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.dependencies.james_director import get_james_director_use_case

logger = logging.getLogger(__name__)

_HERE = Path(__file__).resolve()
_TITANIC_CSV_CANDIDATES: tuple[Path, ...] = (
    _HERE.parents[4] / "app" / "Titanic-Dataset.csv",  # backend/apps/titanic/app/
    _HERE.parents[7] / "frontend" / "apps" / "titanic" / "app" / "Titanic-Dataset.csv",
)


def _normalize_titanic_row(row: dict) -> dict:
    """CSV DictReader 한 행을 `JamesDirectorPassengerRow` 필드명에 맞춘 dict 로 변환 (무상태)."""
    normalized: dict = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        key = raw_key.strip()
        if key.startswith("\ufeff"):
            key = key[1:].strip()
        lower_key = key.lower()
        if lower_key == "sex":
            normalized["gender"] = value
        elif lower_key == "passengerid":
            normalized["passenger_id"] = value
        elif lower_key == "sibsp":
            normalized["sib_sp"] = value
        elif lower_key in {
            "survived",
            "pclass",
            "name",
            "age",
            "parch",
            "ticket",
            "fare",
            "cabin",
            "embarked",
            "gender",
        }:
            normalized[lower_key] = value
        else:
            normalized[key] = value
    return normalized


def build_james_upload_records_from_bytes(*, filename: str, raw: bytes) -> JamesDirectorRecordsSchema:
    """업로드 바이트만으로 `JamesDirectorRecordsSchema` 를 만든다. 전역·DB·로거에 접근하지 않음.

    잘못된 입력은 모두 `ValueError` (메시지를 HTTP 400 detail 로 쓸 수 있음).
    """
    fn = filename.strip()
    if not fn.lower().endswith(".csv"):
        raise ValueError("CSV 파일(.csv)만 업로드해주세요.")

    text = raw.decode("utf-8", errors="replace")
    if text.startswith("\ufeff"):
        text = text[1:]
    if not text.strip():
        raise ValueError("빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise ValueError("CSV 헤더를 읽을 수 없습니다.")

    rows: list[JamesDirectorPassengerRow] = []
    for row in reader:
        try:
            rows.append(JamesDirectorPassengerRow.model_validate(_normalize_titanic_row(row)))
        except Exception as exc:
            raise ValueError(f"행 파싱 실패: {exc}") from exc

    return JamesDirectorRecordsSchema(filename=fn, rows=rows)


def james_upload_success_response(records: JamesDirectorRecordsSchema) -> JamesDirectorUploadResponse:
    """파싱된 레코드로 성공 응답 DTO 만든다 (무상태)."""
    return JamesDirectorUploadResponse(
        message="CSV를 JamesDirectorRecordsSchema 로 옮겼습니다.",
        filename=records.filename,
        row_count=len(records.rows),
        note="",
    )


james_director_router = APIRouter(prefix="/james", tags=["james"])
# `api/__init__.py` 가 `james_router` 이름으로 묶음
james_router = james_director_router


@james_director_router.post("/upload", response_model=JamesDirectorResponse)
async def upload_titanic_file(
    file: UploadFile = File(...),
    james: JamesDirectorUseCase = Depends(get_james_director_use_case),
) -> JamesDirectorUploadResponse:
    """타이타닉 승객 데이터 CSV 파일 업로드. 파싱·DTO 조립은 무상태 함수에 위임한다."""
    filename = (file.filename or "upload.csv").strip()
    raw = await file.read()
    try:
        records = build_james_upload_records_from_bytes(filename=filename, raw=raw)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    logger.info(
        "[제임스 라우터] 업로드된 CSV에서 스키마로 옮겨진 상위 5개 레코드 (filename=%s)",
        records.filename,
    )
    for record in records.rows[:5]:
        logger.info("%s", record)

    try:
        await james.receive_uploaded_records(records)
    except SQLAlchemyError as exc:
        logger.exception("[제임스 라우터] Neon 저장 실패")
        raise HTTPException(
            status_code=503,
            detail=(
                "Neon/PostgreSQL 저장에 실패했습니다. DATABASE_URL·SSL·`alembic upgrade head` "
                "또는 서버 로그를 확인하세요."
            ),
        ) from exc
    except Exception as exc:
        logger.exception("[제임스 라우터] 업로드 처리 중 예기치 않은 오류")
        raise HTTPException(
            status_code=500,
            detail="서버에서 업로드를 처리하지 못했습니다. 백엔드 로그를 확인하세요.",
        ) from exc

    return await james.upload_titanic_file(records)

@james_director_router.get(
    "/passengers",
    response_model=JamesDirectorPassengersListResponse,
    operation_id="james_list_passengers",
)
async def list_passengers() -> JamesDirectorPassengersListResponse:
    """번들된 `Titanic-Dataset.csv` 기준 승객 목록 (DB 없이 조회)."""
    return _load_passengers_from_dataset()


async def list_passengers_titanic_root() -> JamesDirectorPassengersListResponse:
    """`/titanic/passengers` 전용 별칭 (수업용 UI 등). `list_passengers` 와 동일 응답."""
    return _load_passengers_from_dataset()


def _resolve_titanic_csv() -> Path | None:
    for path in _TITANIC_CSV_CANDIDATES:
        if path.is_file():
            return path
    return None


def _stub_passenger_items() -> list[JamesDirectorPassengerRow]:
    """CSV 가 없을 때 수업용 UI용 최소 샘플."""
    return [
        JamesDirectorPassengerRow(
            passenger_id=1,
            survived=0,
            pclass=3,
            name="Braund, Mr. Owen Harris",
            gender="male",
            age=22.0,
            sib_sp=1,
            parch=0,
            ticket="A/5 21171",
            fare=7.25,
            cabin=None,
            embarked="S",
        ),
        JamesDirectorPassengerRow(
            passenger_id=2,
            survived=1,
            pclass=1,
            name="Cumings, Mrs. John Bradley (Florence Briggs Thayer)",
            gender="female",
            age=38.0,
            sib_sp=1,
            parch=0,
            ticket="PC 17599",
            fare=71.2833,
            cabin="C85",
            embarked="C",
        ),
        JamesDirectorPassengerRow(
            passenger_id=3,
            survived=1,
            pclass=3,
            name="Heikkinen, Miss. Laina",
            gender="female",
            age=26.0,
            sib_sp=0,
            parch=0,
            ticket="STON/O2. 3101282",
            fare=7.925,
            cabin=None,
            embarked="S",
        ),
    ]


def _load_passengers_from_dataset() -> JamesDirectorPassengersListResponse:
    csv_path = _resolve_titanic_csv()
    if csv_path is None:
        logger.warning(
            "승객 목록 CSV 없음 — 후보: %s",
            ", ".join(str(p) for p in _TITANIC_CSV_CANDIDATES),
        )
        return JamesDirectorPassengersListResponse(
            ok=True,
            items=_stub_passenger_items(),
            note="Titanic-Dataset.csv 가 없어 샘플 3건만 반환합니다. `backend/apps/titanic/app/` 등에 CSV 를 두면 전체가 로드됩니다.",
        )
    try:
        text = csv_path.read_text(encoding="utf-8")
    except OSError as exc:
        logger.exception("승객 목록 CSV 읽기 실패")
        return JamesDirectorPassengersListResponse(
            ok=False,
            items=[],
            note=f"파일 읽기 오류: {exc}",
        )
    if text.startswith("\ufeff"):
        text = text[1:]
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        return JamesDirectorPassengersListResponse(
            ok=False,
            items=[],
            note="CSV 헤더를 읽을 수 없습니다.",
        )
    rows: list[JamesDirectorPassengerRow] = []
    try:
        for row in reader:
            rows.append(JamesDirectorPassengerRow.model_validate(_normalize_titanic_row(row)))
    except Exception as exc:
        logger.exception("승객 CSV 파싱 실패")
        return JamesDirectorPassengersListResponse(
            ok=False,
            items=[],
            note=f"파싱 오류: {exc}",
        )
    return JamesDirectorPassengersListResponse(
        ok=True,
        items=rows,
        note=csv_path.name,
    )
