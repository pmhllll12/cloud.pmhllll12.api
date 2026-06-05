from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class WalterRoasterSchemaLike(Protocol):
    """`WalterRoasterSchema` 와 동일 필드를 가진 인바운드 모델 (import 순환·부작용 방지)."""

    id: int
    name: str
    memo: str


@dataclass(frozen=True)
class WalterRoasterDto:
    """`WalterRoasterSchema` 컬럼(id, name, memo)을 애플리케이션 계층에서 다룰 때 사용."""

    id: int = 1
    name: str = "Walter"
    memo: str = "월터는 타이타닉의 승무원이다"

    @classmethod
    def from_schema(cls, schema: WalterRoasterSchemaLike) -> WalterRoasterDto:
        """인바운드 스키마(또는 동일 속성 객체)에서 값을 복사합니다."""
        return cls(id=schema.id, name=schema.name, memo=schema.memo)

@dataclass
class WalterRoasterResponse:
    id: int
    name: str
    memo: str

# 레거시 이름 (기존 `WalterRoasterQuery()` 호출 호환)
WalterRoasterQuery = WalterRoasterDto
