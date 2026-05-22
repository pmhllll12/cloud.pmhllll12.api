"""로컬 API 서버 — `uvicorn` 과 같은 Python 으로 실행하세요.

  cd backend\\apps
  python run_api.py

또는:

  python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
"""

from __future__ import annotations

import os

import uvicorn

API_PORT = int(os.getenv("API_PORT", "8000"))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=API_PORT,
        reload=True,
        reload_dirs=["."],
    )
