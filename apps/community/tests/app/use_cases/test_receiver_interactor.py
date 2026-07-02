from __future__ import annotations

import asyncio
from datetime import datetime

import pytest
from community.app.dtos.receiver_dto import ReceivedEmailLog, ReceiveEmailCommand
from community.app.ports.output.embedding_port import EmbeddingPort
from community.app.ports.output.receiver_port import ReceiverPort
from community.app.use_cases.receiver_interactor import ReceiverInteractor


class _StubEmbedder(EmbeddingPort):
    async def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


class _StubRepository(ReceiverPort):
    def __init__(self) -> None:
        self.saved: list[dict] = []

    async def save(
        self,
        subject: str,
        from_: str | None,
        to: str | None,
        body: str | None,
        received_at: datetime,
        embedding: list[float],
    ) -> None:
        self.saved.append(
            {
                "subject": subject,
                "from_": from_,
                "to": to,
                "body": body,
                "received_at": received_at,
                "embedding": embedding,
            }
        )

    async def list_recent(self, limit: int = 100) -> list[ReceivedEmailLog]:
        return [
            ReceivedEmailLog(
                received_at=row["received_at"].isoformat(),
                subject=row["subject"],
                from_=row["from_"],
                to=row["to"],
                body=row["body"],
            )
            for row in self.saved
        ]


def test_receive_saves_with_embedding():
    async def _run():
        repository = _StubRepository()
        interactor = ReceiverInteractor(repository=repository, embedder=_StubEmbedder())
        result = await interactor.receive(
            ReceiveEmailCommand(subject="제목", from_="a@b.com", to="c@d.com", body="본문")
        )
        return repository, result

    repository, result = asyncio.run(_run())
    assert result.ok is True
    assert len(repository.saved) == 1
    assert repository.saved[0]["subject"] == "제목"
    assert repository.saved[0]["embedding"] == [0.1, 0.2, 0.3]


def test_receive_blank_subject_raises():
    async def _run():
        interactor = ReceiverInteractor(repository=_StubRepository(), embedder=_StubEmbedder())
        return await interactor.receive(
            ReceiveEmailCommand(subject="   ", from_=None, to=None, body=None)
        )

    with pytest.raises(ValueError, match="subject는 비어 있을 수 없습니다"):
        asyncio.run(_run())


def test_get_logs_returns_saved_entries():
    async def _run():
        repository = _StubRepository()
        interactor = ReceiverInteractor(repository=repository, embedder=_StubEmbedder())
        await interactor.receive(
            ReceiveEmailCommand(subject="제목", from_="a@b.com", to=None, body=None)
        )
        return await interactor.get_logs()

    logs = asyncio.run(_run())
    assert len(logs) == 1
    assert logs[0].subject == "제목"
