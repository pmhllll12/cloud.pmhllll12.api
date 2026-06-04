"""Titanic 아웃바운드 ORM — `database.Base` 메타데이터 등록용."""

from titanic.adapter.outbound.orm.booking_orm import JamesBooking
from titanic.adapter.outbound.orm.person_orm import JamesPerson

__all__ = ["JamesBooking", "JamesPerson"]
