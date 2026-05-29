import asyncio
import logging
import os
import re
import sys
from pathlib import Path

# `backend/` 에서 실행: `main` 모듈은 이 파일, `adapters`·`titanic` 등은 `apps/` 에 있음
_BACKEND_ROOT = Path(__file__).resolve().parent
_APPS_ROOT = _BACKEND_ROOT / "apps"
_backend_str = str(_BACKEND_ROOT)
_apps_str = str(_APPS_ROOT)
if _backend_str not in sys.path:
    sys.path.insert(0, _backend_str)
if _apps_str not in sys.path:
    sys.path.append(_apps_str)

# Windows: NumPy/BLAS·MKL 이 기본 멀티스레드일 때 일부 환경에서 프로세스가 네이티브 크래시로
# 종료되는 경우가 있어, pandas/numpy 로드 전에 스레드 수를 1로 제한합니다.
if sys.platform == "win32":
    for _k in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
    ):
        os.environ.setdefault(_k, "1")

from _import_aliases import install_secom_aliases  # noqa: E402

install_secom_aliases()

# Windows: psycopg 비동기는 ProactorEventLoop 와 호환되지 않음
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.db_health_adapter import DbHealthAdapter
from adapters.weather_adapter import fetch_seoul_weather
from database import dispose_engine, get_db
from doro.app.doro_director import DoroDirector
from matrix.app.keymaker import MissingApiKeyError, format_gemini_error, keymaker
from titanic.adapter.inbound.api.V1.james_router import james_router
from titanic.adapter.inbound.api.V1.titanic_query_router import router as titanic_query_router
from titanic.adapter.inbound.api.V1.walter_router import walter_router
from secom.app.controllers.user_controller import UserController, register_secom_routes
from secom.app.repositories.user_repository import UserRepository
from secom.schemas.user_schemas import UserSchemas
from secom.app.services.user_service import UserService
from logging_config import get_uvicorn_log_config, setup_app_logging

setup_app_logging()
logger = logging.getLogger(__name__)
API_PORT = int(os.getenv("API_PORT", "8000"))
# 폰·다른 PC에서 `http://<이_PC_LAN_IP>:8000` 으로 직접 호출할 때는 0.0.0.0 (보안: 신뢰 네트워크에서만)
API_HOST = os.getenv("API_HOST", "127.0.0.1").strip() or "127.0.0.1"
_SIGNUP_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class SignupRequest(BaseModel):
    """회원가입 POST 본문."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "newuser01",
                "email": "newuser@example.com",
                "nickname": "홍길동",
                "phone": "01012345678",
                "password": "password12",
                "password_confirm": "password12",
            }
        }
    )

    user_id: str = Field(
        ...,
        min_length=2,
        max_length=64,
        description="로그인 아이디",
        examples=["newuser01"],
    )
    email: str = Field(
        ...,
        min_length=3,
        max_length=320,
        description="도메인에 점(.)이 있는 이메일 (예: user@example.com)",
        examples=["newuser@example.com"],
    )
    nickname: str = Field(
        ...,
        min_length=1,
        max_length=64,
        examples=["홍길동"],
    )
    phone: str = Field(
        ...,
        min_length=9,
        max_length=32,
        description="숫자만 또는 하이픈 포함 (예: 010-1234-5678)",
        examples=["01012345678"],
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=512,
        examples=["password12"],
    )
    password_confirm: str = Field(
        ...,
        min_length=6,
        max_length=512,
        examples=["password12"],
    )


class SignupResponse(BaseModel):
    ok: bool
    message: str
    email: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_app_logging()
    from secom.app.bootstrap import init_secom_db

    await init_secom_db()
    logger.info(
        "API 준비 port=%s — docs http://127.0.0.1:%s/docs | ping http://127.0.0.1:%s/ping",
        API_PORT,
        API_PORT,
        API_PORT,
    )
    logger.info(
        "프론트는 별도 터미널에서 저장소 루트 `npm run dev` 또는 `frontend` 에서 `npm run dev` 로 실행하세요. "
        "해당 터미널을 닫거나 Ctrl+C 하면 http://localhost:3000 은 연결 거부(ERR_CONNECTION_REFUSED)가 됩니다. "
        "자세한 안내: frontend/DEV_SERVER.md"
    )
    try:
        yield
    finally:
        await dispose_engine()


app = FastAPI(title="TJ Watson Main Page", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_secom_routes(app)

app.include_router(titanic_query_router, prefix="/titanic", tags=["titanic"])
app.include_router(james_router)
app.include_router(walter_router)


@app.middleware("http")
async def log_http_requests(request: Request, call_next):
    logger.info("HTTP >>> %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("HTTP <<< %s %s status=%s", request.method, request.url.path, response.status_code)
    return response


@app.get("/ping")
def ping() -> dict[str, bool]:
    """브라우저에서 열면 요청 로그가 찍히는지 확인용."""
    logger.info("[ping] 요청 수신 — 로깅 정상")
    return {"ok": True}


@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}


@app.post("/signup", response_model=SignupResponse)
async def signup(
    body: SignupRequest,
    db: AsyncSession = Depends(get_db),
) -> SignupResponse:
    """회원가입 — 검증 후 secom 레이어(controller → service → repository)로 저장합니다."""
    email = body.email.strip()
    if not _SIGNUP_EMAIL_RE.match(email):
        logger.warning(
            "[/signup] 이메일 형식 거부 — email=%r (save_user 미호출)",
            email,
        )
        raise HTTPException(status_code=422, detail="올바른 이메일 형식이 아닙니다.")
    if body.password != body.password_confirm:
        logger.warning(
            "[/signup] 비밀번호 불일치 — email=%r (save_user 미호출)",
            email,
        )
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")

    logger.info(
        "[/signup] 요청 수신 — user_id=%s email=%s nickname=%s phone=%s",
        body.user_id.strip(),
        email,
        body.nickname.strip(),
        body.phone.strip(),
    )

    user_schemas = UserSchemas(
        user_id=body.user_id.strip(),
        email=body.email,
        nickname=body.nickname.strip(),
        phone=body.phone.strip(),
        password=body.password,
        password_confirm=body.password_confirm,
        role="user",
    )
    try:
        user_service = UserService(UserRepository(db))
        await UserController(user_service).save_user(user_schemas)
    except ValueError as exc:
        if db.in_transaction():
            await db.rollback()
        logger.warning("[/signup] 검증 실패 — %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except IntegrityError as exc:
        if db.in_transaction():
            await db.rollback()
        logger.warning("[/signup] 중복 데이터 — %s", exc.orig)
        raise HTTPException(
            status_code=409,
            detail="이미 사용 중인 아이디 또는 이메일입니다.",
        ) from exc
    except SQLAlchemyError as exc:
        if db.in_transaction():
            await db.rollback()
        logger.exception("[/signup] DB 오류")
        raise HTTPException(
            status_code=503,
            detail="데이터베이스 연결 오류입니다. 잠시 후 다시 시도하세요.",
        ) from exc

    return SignupResponse(
        ok=True,
        message="회원가입 요청이 접수되었습니다.",
        email=email,
    )


class ChatRequest(BaseModel):
    """클라이언트가 보내는 사용자 메시지."""

    message: str = Field(..., min_length=1, max_length=100_000)


class ChatResponse(BaseModel):
    """Gemini 모델의 텍스트 응답."""

    reply: str
    model: str


class WeatherResponse(BaseModel):
    """서울 현재 날씨."""

    city: str
    temp: int
    description: str
    icon: str


def _extract_text(response: Any) -> str:
    try:
        text = (response.text or "").strip()
    except ValueError:
        text = ""
    if text:
        return text
    if response.candidates:
        parts = response.candidates[0].content.parts
        chunks = [getattr(p, "text", "") or "" for p in parts]
        return "".join(chunks).strip()
    return ""


@app.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    """JSON `{"message": "..."}` 를 받아 Gemini 답변을 JSON으로 반환합니다."""
    def _generate():
        return keymaker.generate_content(body.message)

    try:
        response, model_used = await asyncio.to_thread(_generate)
    except MissingApiKeyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        status, detail = format_gemini_error(exc)
        raise HTTPException(status_code=status, detail=detail) from exc

    reply = _extract_text(response)
    if not reply:
        raise HTTPException(status_code=502, detail="모델이 비어 있는 응답을 반환했습니다.")
    return ChatResponse(reply=reply, model=model_used)


@app.get("/weather", response_model=WeatherResponse)
async def weather() -> WeatherResponse:
    """서울 현재 온도·날씨 아이콘 코드(OpenWeatherMap)."""

    def _fetch():
        return fetch_seoul_weather()

    try:
        data = await asyncio.to_thread(_fetch)
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return WeatherResponse(**data)


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    return await DbHealthAdapter.neon_time_check(db)


@app.get("/doro/data")
def read_doro_data():
    doro_director = DoroDirector()
    df = doro_director.get_data()

    return df.to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn

    setup_app_logging()
    # Windows + reload 시 WatchFiles 가 서버를 자주 끊어 Vite 프록시 502 가 남 → 기본 끔
    _reload_default = "0" if sys.platform == "win32" else "1"
    use_reload = os.getenv("UVICORN_RELOAD", _reload_default).lower() in (
        "1",
        "true",
        "yes",
    )
    if use_reload:
        logger.info("uvicorn reload=ON (코드 저장 시 재시작)")
    else:
        logger.info(
            "uvicorn reload=OFF — 안정 실행. 자동 재시작은 UVICORN_RELOAD=1"
        )
    _uvicorn_kwargs = dict(
        host=API_HOST,
        port=API_PORT,
        log_level="info",
        log_config=get_uvicorn_log_config(),
        access_log=True,
    )
    if use_reload:
        uvicorn.run(
            "main:app",
            reload=True,
            reload_dirs=[str(_BACKEND_ROOT), str(_APPS_ROOT)],
            **_uvicorn_kwargs,
        )
    else:
        uvicorn.run(app, **_uvicorn_kwargs)
