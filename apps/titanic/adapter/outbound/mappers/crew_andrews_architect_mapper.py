from __future__ import annotations

from titanic.domain.entities.crew_andrews_architect_entity import AndrewsArchitectEntity


def andrews_architect_default_entity() -> AndrewsArchitectEntity:
    """`AndrewsArchitectOrm` 이 `__abstract__` 이므로 기본 엔티티만 제공합니다."""
    return AndrewsArchitectEntity()


__all__ = ["andrews_architect_default_entity"]
