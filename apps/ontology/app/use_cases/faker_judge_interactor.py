from __future__ import annotations

import asyncio
import logging
import re

from core.lol.t1_mid_faker_orchestrator import FakerOrchestrator
from ontology.app.ports.input.judge_use_case import JudgeUseCase
from ontology.domain.evidence import Evidence
from ontology.domain.verdict import Verdict

logger = logging.getLogger(__name__)

_VERDICT_RE = re.compile(r"VERDICT\s*:\s*(SPAM|HAM)", re.IGNORECASE)
_REASON_RE = re.compile(r"REASON\s*:\s*(.+)", re.IGNORECASE)


def _parse_verdict(reply: str) -> Verdict:
    verdict_match = _VERDICT_RE.search(reply)
    label = verdict_match.group(1).upper() if verdict_match else (
        "SPAM" if "SPAM" in reply.upper() else "HAM"
    )
    reason_match = _REASON_RE.search(reply)
    reason = reason_match.group(1).strip() if reason_match else reply[:120].strip()
    confidence = 0.88 if label == "SPAM" else 0.12
    return Verdict(label=label, confidence=confidence, reason=reason)


class FakerJudgeInteractor(JudgeUseCase):
    """EXAONE 3.5:2.4b(FakerOrchestrator)로 Evidence를 판정하는 인터렉터."""

    def __init__(self, orchestrator: FakerOrchestrator) -> None:
        self._orchestrator = orchestrator

    async def evaluate(self, evidence: Evidence) -> Verdict:
        prompt = f"판정 대상 신호: {evidence.signals}"
        reply = await asyncio.to_thread(self._orchestrator.chat, prompt)
        verdict = _parse_verdict(reply)
        logger.info(
            "[FakerJudgeInteractor] source=%s label=%s confidence=%.2f",
            evidence.source_app,
            verdict.label,
            verdict.confidence,
        )
        return verdict
