"""OpenWeatherMap — 서울 현재 날씨."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

_APPS_ROOT = Path(__file__).resolve().parent.parent


def _load_env() -> None:
    load_dotenv(_APPS_ROOT / ".env")
    load_dotenv()


def get_openweather_api_key() -> str | None:
    _load_env()
    for name in ("OPENWEATHER_API_KEY", "VITE_OPENWEATHER_API_KEY"):
        raw = (os.getenv(name) or "").strip()
        if raw:
            return raw
    return None


def fetch_seoul_weather() -> dict[str, str | int]:
    key = get_openweather_api_key()
    if not key:
        raise ValueError(
            "OPENWEATHER_API_KEY 가 없습니다. backend/apps/.env 에 키를 설정하세요."
        )

    q = urllib.parse.urlencode(
        {
            "q": "Seoul,KR",
            "units": "metric",
            "lang": "kr",
            "appid": key,
        }
    )
    url = f"https://api.openweathermap.org/data/2.5/weather?{q}"

    try:
        with urllib.request.urlopen(url, timeout=12) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise ValueError(body or f"OpenWeather HTTP {exc.code}") from exc

    w = (payload.get("weather") or [{}])[0]
    main = payload.get("main") or {}
    temp = main.get("temp")
    if temp is None:
        raise ValueError("온도 정보가 없습니다.")

    return {
        "city": "서울",
        "temp": int(round(float(temp))),
        "description": str(w.get("description") or "날씨"),
        "icon": str(w.get("icon") or "01d"),
    }
