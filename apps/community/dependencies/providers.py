from __future__ import annotations

import os

from community.adapter.outbound.n8n_email_client import N8nEmailClient

_DEFAULT_WEBHOOK = "http://localhost:5678/webhook/community-email"


def get_n8n_email_client() -> N8nEmailClient:
    url = os.getenv("N8N_COMMUNITY_EMAIL_WEBHOOK_URL", _DEFAULT_WEBHOOK)
    return N8nEmailClient(webhook_url=url)
