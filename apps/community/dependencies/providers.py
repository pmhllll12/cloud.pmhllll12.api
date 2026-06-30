from __future__ import annotations

import os

from community.adapter.outbound.n8n_email_client import N8nEmailClient
from community.app.ports.input.community_host_use_case import CommunityHostUseCase
from community.app.ports.input.discord_use_case import DiscordUseCase
from community.app.ports.input.email_host_use_case import EmailHostUseCase
from community.app.ports.input.juso_use_case import JusoUseCase
from community.app.ports.input.send_email_use_case import SendEmailUseCase
from community.app.ports.input.telegram_use_case import TelegramUseCase
from community.app.use_cases.community_host_interactor import CommunityHostInteractor
from community.app.use_cases.discord_interactor import DiscordInteractor
from community.app.use_cases.email_host_interactor import EmailHostInteractor
from community.app.use_cases.juso_interactor import JusoInteractor
from community.app.use_cases.send_email_interactor import SendEmailInteractor
from community.app.use_cases.telegram_interactor import TelegramInteractor

_DEFAULT_WEBHOOK = "http://localhost:5678/webhook/community-email"


def get_send_email_use_case() -> SendEmailUseCase:
    url = os.getenv("N8N_COMMUNITY_EMAIL_WEBHOOK_URL", _DEFAULT_WEBHOOK)
    return SendEmailInteractor(client=N8nEmailClient(webhook_url=url))


def get_community_host_use_case() -> CommunityHostUseCase:
    return CommunityHostInteractor()


def get_juso_use_case() -> JusoUseCase:
    return JusoInteractor()


def get_discord_use_case() -> DiscordUseCase:
    return DiscordInteractor()


def get_telegram_use_case() -> TelegramUseCase:
    return TelegramInteractor()


def get_email_host_use_case() -> EmailHostUseCase:
    return EmailHostInteractor()
