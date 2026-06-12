# 백엔드 (`minho`) — LLM 코딩 지침

FastAPI 백엔드 워크스페이스. 진입점은 [`main.py`](main.py) 이고, 도메인 코드는 [`apps/`](apps/) 아래 **시블링 앱**으로 둔다.

공통 4원칙 전문 ---> [`../vault/CLAUDE.md`](../vault/CLAUDE.md)  
에이전트 하네스 ---> [`../vault/AGENTS.md`](../vault/AGENTS.md)  
모노레포 지도 ---> [`../CLAUDE.md`](../CLAUDE.md)

---

## 디렉터리

| 경로 | 역할 |
|------|------|
| `main.py` | FastAPI 앱, `titanic_router` 등 마운트 |
| `apps/` | 도메인 패키지 (`titanic`, 추후 `soccer` …) |
| `core/` | `matrix` 등 공통 모듈 |
| `alembic/` | DB 마이그레이션 |
| `database.py` | SQLAlchemy 엔진·세션 |
| `.env` | `DATABASE_URL`, `GEMINI_API_KEY`, `API_PORT` 등 |
| `docker_entrypoint.py` | Docker: alembic(선택) + uvicorn |

---

## `apps/` 시블링 구조

```
minho/apps/
├── titanic/          # 타이타닉 데모 (헥사고날)
│   ├── .cursorrules
│   └── _docs/CLAUDE.md
└── <future-app>/     # 새 앱은 같은 층에 추가
```

- 앱 간 **직접 import 금지**를 기본으로 하고, `main.py`에서 라우터만 `include_router` 한다.
- 앱별 규칙은 **`minho/apps/<앱>/.cursorrules`** 와 **`_docs/CLAUDE.md`** 에 둔다.

타이타닉 상세 ---> [`apps/titanic/_docs/CLAUDE.md`](apps/titanic/_docs/CLAUDE.md)

---

## 실행

### 로컬

```powershell
cd minho
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

- 문서: `http://127.0.0.1:8000/docs`
- 헬스: `http://127.0.0.1:8000/ping`

### Docker (루트)

```powershell
cd ..
docker compose up --build -d
```

- 브라우저 UI: `http://localhost:3000` (gateway)
- API 직접: `http://localhost:8000` (compose 포트 매핑 시)

게이트웨이·Docker 오류 ---> [`../docker/README.md`](../docker/README.md)

---

## API 경로 (프록시와 맞출 것)

- `titanic_router` prefix는 **`/titanic`** (`/api/titanic` 아님).
- 게이트웨이 `location ^~ /titanic/` 과 Vite `www/vite.config.ts` 프록시가 **URI를 그대로** 백엔드로 넘긴다.
- 예: `POST /titanic/smith/chat`, `POST /titanic/james/upload`

---

## 백엔드 규약 (vault)

| 주제 | 정본 |
|------|------|
| 엔티티·PK | [`../vault/DevOps/Backend/ENTITY_RULE.md`](../vault/DevOps/Backend/ENTITY_RULE.md) |
| Alembic | [`alembic/README.md`](alembic/README.md) |

---

## 환경 변수 (요약)

| 변수 | 용도 |
|------|------|
| `DATABASE_URL` | Neon/PostgreSQL |
| `GEMINI_API_KEY` | 스미스 채팅 등 Gemini |
| `API_HOST` | Docker: `0.0.0.0` |
| `API_PORT` | 기본 `8000` |
