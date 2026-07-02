from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from community.adapter.outbound.gemini_embedding_client import GeminiEmbeddingClient
from community.adapter.outbound.repositories.receiver_repository import ReceiverRepository
from community.app.ports.input.receiver_use_case import ReceiverUseCase
from community.app.ports.output.embedding_port import EmbeddingPort
from community.app.ports.output.receiver_port import ReceiverPort
from community.app.use_cases.receiver_interactor import ReceiverInteractor
from database import get_db


def get_receiver_repository(
    db: AsyncSession = Depends(get_db),
) -> ReceiverPort:
    return ReceiverRepository(session=db)


def get_embedding_port() -> EmbeddingPort:
    return GeminiEmbeddingClient()


def get_receiver_use_case(
    repository: ReceiverPort = Depends(get_receiver_repository),
    embedder: EmbeddingPort = Depends(get_embedding_port),
) -> ReceiverUseCase:
    return ReceiverInteractor(repository=repository, embedder=embedder)
