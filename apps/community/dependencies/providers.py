from __future__ import annotations

import os

from community.adapter.outbound.n8n_email_client import N8nEmailClient
from community.app.ports.input.send_email_use_case import SendEmailUseCase
from community.app.use_cases.send_email_interactor import SendEmailInteractor

_DEFAULT_WEBHOOK = "http://localhost:5678/webhook/community-email"


def get_send_email_use_case() -> SendEmailUseCase:
    url = os.getenv("N8N_COMMUNITY_EMAIL_WEBHOOK_URL", _DEFAULT_WEBHOOK)
    return SendEmailInteractor(client=N8nEmailClient(webhook_url=url))
