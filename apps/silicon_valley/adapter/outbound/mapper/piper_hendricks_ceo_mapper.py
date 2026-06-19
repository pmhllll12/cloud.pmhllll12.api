from __future__ import annotations

from silicon_valley.domain.entities.piper_hendricks_ceo_entity import HendricksCeoEntity


def hendricks_ceo_default_entity() -> HendricksCeoEntity:
    return HendricksCeoEntity()


__all__ = ["hendricks_ceo_default_entity"]
