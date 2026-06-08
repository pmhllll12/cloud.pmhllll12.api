"""Titanic application output ports."""

from titanic.app.ports.output.walter_repository import (
    WalterPersistPayload,
    WalterRepositoryPort,
    submit_fetch_all_passengers,
    submit_persist_upload as submit_walter_persist_upload,
)

__all__ = [
    "submit_walter_persist_upload",
    "WalterPersistPayload",
    "WalterRepositoryPort",
    "submit_fetch_all_passengers",
]
