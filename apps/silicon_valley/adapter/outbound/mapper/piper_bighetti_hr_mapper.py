from __future__ import annotations

from silicon_valley.domain.entities.piper_bighetti_hr_entity import BighettiHrEntity


def bighetti_hr_default_entity() -> BighettiHrEntity:
    return BighettiHrEntity()


__all__ = ["bighetti_hr_default_entity"]
