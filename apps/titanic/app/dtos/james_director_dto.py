"""Titanic 3NF ERD 기반 James 커맨드 DTO.

직렬화·경계 계층 단순화를 위해 스칼라는 모두 str 로 둡니다.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class PersonCommand(BaseModel):
    """Person 엔티티에 대응. Booking·Port 는 FK 문자열만 포함."""

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    passenger_id: str
    booking_id: str
    embarked_code: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


class BookingCommand(BaseModel):
    """Booking 에 Port(승선지)를 붙인 역정규화 스냅샷. country 는 포함하지 않습니다."""

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    booking_id: str
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked_code: str
    port_name: str


__all__ = ["BookingCommand", "PersonCommand"]
