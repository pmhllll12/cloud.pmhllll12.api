"""로컬 Titanic CSV → Neon `titanic_james_passengers` 적재.

  cd backend\\apps
  python scripts/import_titanic_to_neon.py
  python scripts/import_titanic_to_neon.py "C:\\Users\\hi\\Downloads\\Titanic-Dataset.csv"
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

_APPS = Path(__file__).resolve().parent.parent
_BACKEND = _APPS.parent

for _entry in (str(_APPS), str(_BACKEND)):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

os.chdir(_BACKEND)

from _import_aliases import install_secom_aliases  # noqa: E402

install_secom_aliases()


async def _run(csv_path: Path) -> None:
    from database import AsyncSessionLocal, create_all_tables, engine
    from friday13th.app.bootstrap import init_secom_db
    from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
    from titanic.app.ports.input.james_use_case import JamesUploadInput
    from titanic.app.use_cases.james_command import JamesCommand, james_repository_ctx

    if engine is None or AsyncSessionLocal is None:
        raise SystemExit(
            "DATABASE_URL 이 없거나 엔진 초기화에 실패했습니다. backend/.env 를 확인하세요."
        )

    if not csv_path.is_file():
        raise SystemExit(f"CSV 파일을 찾을 수 없습니다: {csv_path}")

    await init_secom_db()
    content = csv_path.read_bytes()
    filename = csv_path.name

    async with AsyncSessionLocal() as session:
        repo = JamesPgRepository(session=session)
        token = james_repository_ctx.set(repo)
        try:
            command = JamesCommand()
            result = await command.receive_uploaded_records(
                JamesUploadInput(content=content, filename=filename)
            )
        finally:
            james_repository_ctx.reset(token)

    print(f"OK - {result.message}")
    print(f"file: {result.filename}, rows: {result.row_count}")
    print(f"columns: {', '.join(result.columns)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Titanic CSV → Neon 적재")
    parser.add_argument(
        "csv",
        nargs="?",
        default=r"C:\Users\hi\Downloads\Titanic-Dataset.csv",
        help="CSV 경로 (기본: Downloads/Titanic-Dataset.csv)",
    )
    args = parser.parse_args()
    asyncio.run(_run(Path(args.csv).expanduser().resolve()))


if __name__ == "__main__":
    main()
