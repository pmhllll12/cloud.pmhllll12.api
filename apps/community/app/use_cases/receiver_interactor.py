from __future__ import annotations

import logging
from datetime import datetime

from community.app.dtos.receiver_dto import (
    ReceivedEmailLog,
    ReceiveEmailCommand,
    ReceiveEmailResult,
)
from community.app.ports.input.receiver_use_case import ReceiverUseCase
from community.app.ports.output.embedding_port import EmbeddingPort
from community.app.ports.output.receiver_port import ReceiverPort
from community.domain.received_email import ReceivedEmail

logger = logging.getLogger(__name__)


class ReceiverInteractor(ReceiverUseCase):
    def __init__(self, repository: ReceiverPort, embedder: EmbeddingPort) -> None:
        self.repository = repository
        self.embedder = embedder

    async def receive(self, command: ReceiveEmailCommand) -> ReceiveEmailResult:
        email = ReceivedEmail(
            subject=command.subject,
            from_=command.from_,
            to=command.to,
            body=command.body,
            received_at=datetime.now(),
        )
        embedding = await self.embedder.embed(f"{email.subject}\n{email.body or ''}")
        await self.repository.save(
            subject=email.subject,
            from_=email.from_,
            to=email.to,
            body=email.body,
            received_at=email.received_at,
            embedding=embedding,
        )
        logger.info("[ReceiverInteractor] receive subject=%r from=%r", email.subject, email.from_)
        return ReceiveEmailResult(ok=True, message="received")

    async def get_logs(self) -> list[ReceivedEmailLog]:
        return await self.repository.list_recent()
