from __future__ import annotations

import asyncio
import logging
import re

import ollama

from community.app.ports.output.content_filter_port import ContentFilterPort

logger = logging.getLogger(__name__)

# Ollama 모델 태그 — meta-llama/Llama-3.1-8B-Instruct 에 대응.
# 미설치 시 `ollama pull llama3.1:8b` 로 먼저 받아야 한다.
_FILTER_MODEL = "llama3.1:8b"

_VERDICT_RE = re.compile(r"VERDICT\s*:\s*(NORMAL|BLOCK)", re.IGNORECASE)

_SYSTEM_PROMPT = (
    "당신은 이메일/메시지 콘텐츠 필터입니다. 아래 텍스트를 NORMAL 또는 BLOCK 으로 판정하세요.\n"
    "BLOCK 기준: 욕설·비속어·모욕, 명백한 스팸/광고, 피싱, 불법 콘텐츠, 협박.\n"
    "NORMAL 기준: 업무 연락, 인사, 칭찬, 감탄사, 일반 문의, 짧은 잡담 등 그 외 모든 것.\n"
    "애매하면 NORMAL로 판정하세요.\n\n"
    "예시:\n"
    "입력: 회의는 3시입니다 → VERDICT: NORMAL\n"
    "입력: 씨발 개새끼야 → VERDICT: BLOCK\n"
    "입력: 넌 천재야 → VERDICT: NORMAL\n"
    "입력: 무료 쿠폰 지금 클릭하세요 http://spam.xyz → VERDICT: BLOCK\n\n"
    "반드시 마지막 줄에 VERDICT: NORMAL 또는 VERDICT: BLOCK 만 출력하세요."
)

# LLM 판정 전 확실한 비속어를 빠르게 걸러내는 스톱워드 사전 (LLM이 짧은 욕설을
# 문맥 없이 정상으로 오판하는 사례가 있어, 명확한 케이스는 LLM 호출 없이 즉시 차단).
_STOP_WORDS = (
    "씨발", "씨팔", "시발", "시팔", "개새끼", "개새기", "병신", "븅신", "지랄",
    "좆", "쓰레기새끼", "머저리", "미친놈", "미친년", "닥쳐", "죽여버린다", "죽여버릴",
)
_STOP_WORD_RE = re.compile("|".join(re.escape(word) for word in _STOP_WORDS))


class LlamaContentFilterClient(ContentFilterPort):
    """스톱워드 사전 + Llama-3.1-8B-Instruct(Ollama `llama3.1:8b`)로
    수신 콘텐츠를 정상/차단 판정한다."""

    def __init__(self, model: str = _FILTER_MODEL) -> None:
        self.model = model

    async def is_normal(self, content: str) -> bool:
        if _STOP_WORD_RE.search(content):
            logger.info("[LlamaContentFilterClient] pre-check verdict=BLOCK (stop word)")
            return False

        reply = await asyncio.to_thread(self._chat, content)
        match = _VERDICT_RE.search(reply)
        # 명확한 비속어는 위 스톱워드 사전이 이미 걸러내므로, 응답 형식이 어긋나는
        # 드문 경우는 오탐(false block) 방지를 위해 NORMAL 쪽으로 판정한다.
        verdict = match.group(1).upper() if match else "NORMAL"
        logger.info("[LlamaContentFilterClient] model=%s verdict=%s", self.model, verdict)
        return verdict == "NORMAL"

    def _chat(self, content: str) -> str:
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": content},
                ],
            )
        except ollama.ResponseError as exc:
            status = getattr(exc, "status_code", None)
            if status == 404:
                raise RuntimeError(
                    f"모델을 찾을 수 없습니다: {self.model!r}\n"
                    f"  ollama pull {self.model}  로 먼저 설치하세요."
                ) from exc
            raise

        if hasattr(response, "message") and response.message is not None:
            return (response.message.content or "").strip()
        if isinstance(response, dict):
            return str(response.get("message", {}).get("content", "")).strip()
        return ""
