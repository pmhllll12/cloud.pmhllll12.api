"""타이타닉 조회(쿼리) HTTP 인바운드 어댑터."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from titanic.app.ports.input.titanic_query_port import TitanicQueryPort
from titanic.app.use_cases.titanic_query_impl import TitanicQueryImpl

router = APIRouter()


def get_titanic_query_port() -> TitanicQueryPort:
    return TitanicQueryImpl()


@router.get("/problem")
def read_titanic_problem(
    port: Annotated[TitanicQueryPort, Depends(get_titanic_query_port)],
) -> dict[str, object]:
    """문제 정의·컬럼 설명(교육·수업용)."""
    return port.get_problem_payload()


@router.get("/data")
def read_titanic_data(
    port: Annotated[TitanicQueryPort, Depends(get_titanic_query_port)],
):
    return port.get_passenger_data_records()


@router.get("/count")
def read_titanic_count(
    port: Annotated[TitanicQueryPort, Depends(get_titanic_query_port)],
):
    return {"count": port.get_passenger_count()}


@router.get("/tree")
def read_titanic_tree(
    port: Annotated[TitanicQueryPort, Depends(get_titanic_query_port)],
):
    return {"tree": port.has_decision_tree_model()}


@router.get("/model")
def read_titanic_model(
    port: Annotated[TitanicQueryPort, Depends(get_titanic_query_port)],
):
    return JSONResponse(content=jsonable_encoder(port.get_model_metrics()))
