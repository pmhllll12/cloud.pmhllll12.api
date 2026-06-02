"""James director — Titanic CSV 업로드 (`/titanic/james`)."""

from __future__ import annotations

import csv
from io import StringIO

from fastapi import APIRouter, File, HTTPException, UploadFile

from titanic.adapter.inbound.api.schemas.james_director_schema import (
    JamesDirectorPassengerRow,
    JamesDirectorRecordsSchema,
    JamesDirectorUploadResponse,
)
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.use_cases.james_director_interactor import JamesDirectorInteractor

james_director_router = APIRouter(prefix="/james", tags=["james"])
# `api/__init__.py` 가 `james_router` 이름으로 묶음
james_router = james_director_router


@james_director_router.post("/upload", response_model=JamesDirectorUploadResponse)
async def upload_titanic_file(file: UploadFile = File(...)) -> JamesDirectorUploadResponse:
    """타이타닉 승객 데이터 CSV 파일 업로드."""
    filename = (file.filename or "upload.csv").strip()
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일(.csv)만 업로드해주세요.")

    raw = await file.read()
    text = raw.decode("utf-8", errors="replace")
    if text.startswith("\ufeff"):
        text = text[1:]
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    rows: list[JamesDirectorPassengerRow] = []
    for row in reader:
        try:
            rows.append(JamesDirectorPassengerRow.model_validate(_normalize_titanic_row(row)))
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"행 파싱 실패: {exc}") from exc

    records = JamesDirectorRecordsSchema(filename=filename, rows=rows)

    print("[제임스 라우터] 업로드된 CSV에서 스키마로 옮겨진 상위 5개 레코드:", flush=True)
    for record in records.rows[:5]:
        print(record, flush=True)

    use_case: JamesDirectorUseCase = JamesDirectorInteractor()
    await use_case.receive_uploaded_records(records)

    return JamesDirectorUploadResponse(
        message="CSV를 JamesDirectorRecordsSchema 로 옮겼습니다.",
        filename=records.filename,
        row_count=len(records.rows),
        note="",
    )


def _normalize_titanic_row(row: dict) -> dict:
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
