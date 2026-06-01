"""James — Titanic CSV·승객 API (`/titanic/james`). 스키마: `james_director_schemas`."""

from __future__ import annotations

import csv
import io
import json
import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from titanic.adapter.inbound.api.schemas.james_director_schemas import (
    JamesDirectorPassengersListResponse,
    JamesDirectorPassengerRow,
    JamesDirectorRecordsSchema,
    JamesDirectorUploadResponse,
)

# 스크린샷·기존 로그와 동일한 로거 이름(모듈은 `james_director_router` 유지)
_james_router_inbound_log = logging.getLogger("titanic.adapter.inbound.api.V1.james_router")

james_router = APIRouter(prefix="/titanic/james", tags=["james"])

_EXPECTED_HEADERS = frozenset(
    {
        "PassengerId",
        "Survived",
        "Pclass",
        "Name",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "Ticket",
        "Fare",
        "Cabin",
        "Embarked",
    }
)


def _decode_csv_text(content: bytes) -> str:
    """UTF-8 우선, 한국 Windows에서 흔한 CP949/EUC-KR 등으로 폴백합니다."""
    if not content:
        return ""
    for encoding in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("UTF-8·CP949·EUC-KR 로 디코딩할 수 없는 파일입니다.")


def _effective_header_set(headers: list[str]) -> set[str]:
    """필수 헤더 검사용: CSV 가 `Sex` 대신 `gender`/`Gender` 만 있어도 E열 요건을 충족한 것으로 봅니다."""
    s = {str(h).strip() for h in headers if str(h).strip()}
    if "Sex" not in s and ("gender" in s or "Gender" in s):
        s = s | {"Sex"}
    return s


def _normalize_header_row(fieldnames: list[str] | None) -> list[str] | None:
    if not fieldnames:
        return None
    return [str(h).strip() for h in fieldnames]


def _normalize_csv_row(raw: dict[str, str | None]) -> dict[str, str | None]:
    """빈 문자열·공백을 정리하고, 숫자 컬럼에 비어 있으면 기본값을 넣습니다."""
    row: dict[str, str | None] = {}
    for k, v in raw.items():
        if not k:
            continue
        key = str(k).strip()
        if isinstance(v, str):
            row[key] = v.strip() or None
        else:
            row[key] = None

    for key in ("PassengerId", "Survived", "Pclass", "SibSp", "Parch"):
        if row.get(key) in (None, ""):
            raise ValueError(f"필수 숫자 컬럼이 비어 있습니다: {key}")
    if row.get("Fare") in (None, ""):
        row["Fare"] = "0"
    if row.get("Age") in (None, ""):
        row["Age"] = None
    if row.get("Name") in (None, ""):
        raise ValueError("Name 컬럼이 비어 있는 행이 있습니다.")
    if row.get("Ticket") in (None, ""):
        row["Ticket"] = ""
    if row.get("Sex") in (None, "") and row.get("gender") in (None, "") and row.get("Gender") in (None, ""):
        raise ValueError("Sex / gender 가 비어 있는 행이 있습니다.")
    return row


def _preview_rows_json(rows: list[JamesDirectorPassengerRow], limit: int) -> str:
    """터미널에 찍을 파싱 결과 샘플(JSON). 대용량 Name 은 잘라서 로그 폭주를 막습니다."""
    sample: list[dict[str, object]] = []
    for r in rows[:limit]:
        name = r.name
        if len(name) > 60:
            name = name[:57] + "..."
        sample.append(
            {
                "PassengerId": r.passenger_id,
                "Survived": r.survived,
                "gender": r.gender,
                "Name": name,
            }
        )
    return json.dumps(sample, ensure_ascii=False)


def _build_records_schema(content: bytes, filename: str) -> JamesDirectorRecordsSchema:
    """CSV 바이트를 읽어 `JamesDirectorRecordsSchema` 로 옮깁니다 (Sex 열은 `gender` 로 검증)."""
    if not content.strip():
        raise ValueError("파일이 비어 있습니다.")
    text = _decode_csv_text(content)

    reader = csv.DictReader(io.StringIO(text))
    headers = _normalize_header_row(reader.fieldnames)
    if not headers:
        raise ValueError("CSV 헤더를 읽을 수 없습니다.")
    header_set = _effective_header_set(headers)
    missing = _EXPECTED_HEADERS - header_set
    if missing:
        raise ValueError(f"필수 컬럼이 없습니다: {', '.join(sorted(missing))}")

    rows: list[JamesDirectorPassengerRow] = []
    for raw in reader:
        if raw is None:
            continue
        base = {str(k).strip(): v for k, v in raw.items() if k}
        if not any((str(v).strip() if v is not None else "") for v in base.values()):
            continue
        try:
            row = _normalize_csv_row(base)
            rows.append(JamesDirectorPassengerRow.model_validate(row))
        except ValueError as exc:
            raise ValueError(f"행 파싱 실패: {exc}") from exc

    if not rows:
        raise ValueError("데이터 행이 없습니다.")

    return JamesDirectorRecordsSchema(filename=filename, rows=rows)


@james_router.post("/upload", response_model=JamesDirectorUploadResponse)
async def upload_titanic_csv(file: UploadFile = File(...)) -> JamesDirectorUploadResponse:
    """타이타닉 승객 데이터 CSV 업로드 — 내용을 `JamesDirectorRecordsSchema` 로 옮겨 담은 뒤 요약을 반환합니다."""
    filename = (file.filename or "").strip()
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    content = await file.read()

    try:
        records: JamesDirectorRecordsSchema = _build_records_schema(content, filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    row_count = len(records.rows)
    preview_n = min(5, row_count)
    _james_router_inbound_log.info(
        "[james_router] 인바운드 - POST /titanic/james/upload 완료 filename=%s rows=%s",
        records.filename,
        row_count,
    )
    _james_router_inbound_log.info(
        "[james_router] 인바운드 - 파싱 레코드 미리보기(상위 %s/%s행): %s",
        preview_n,
        row_count,
        _preview_rows_json(records.rows, preview_n),
    )

    # 추후: records.rows 를 DB·유스케이스로 전달
    _ = records

    return JamesDirectorUploadResponse(
        message="CSV를 JamesDirectorRecordsSchema 로 파싱했습니다. (Sex → gender)",
        filename=records.filename,
        row_count=row_count,
        note="Neon 저장 등은 이후 단계에서 records 를 사용하세요.",
    )


@james_router.get("/passengers", response_model=JamesDirectorPassengersListResponse)
async def list_james_passengers() -> JamesDirectorPassengersListResponse:
    """승객 목록 스텁 — 추후 DB에서 `JamesDirectorPassengerRow` 리스트 반환."""
    return JamesDirectorPassengersListResponse()
