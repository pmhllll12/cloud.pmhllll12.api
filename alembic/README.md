# Alembic (Neon / PostgreSQL)

`DATABASE_URL` 이 `backend/apps/.env` 또는 `backend/.env` 에 있어야 합니다.  
`alembic/env.py` 가 **`backend/apps`** 를 `sys.path` 에 넣어 `titanic` 패키지를 찾습니다.

```bash
cd backend
alembic upgrade head
```

초기 리비전 `20260204_0001` 은 `titanic_persons`, `titanic_bookings` 테이블을 만듭니다.  
이전 이름(`titanic_james_*`)으로 이미 만들어진 DB는 `20260520_0002` 가 테이블·인덱스 이름만 바꿉니다.  
앱 기동 시 `friday_13th` 부트스트랩의 `create_all` 로도 동일 ORM 메타데이터가 생성될 수 있습니다.
