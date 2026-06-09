from __future__ import annotations
from dataclasses import dataclass
from domain.exceptions.domain_exceptions import InvalidValueObjectError


@dataclass(frozen=True)
class JackTrainerId:
    """
    JackTrainer 식별자 Value Object.
    - 불변(frozen=True)
    - 빈 문자열 및 None 불허
    - 동등성은 값으로 판단
    """
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise InvalidValueObjectError(
                f"JackTrainerId는 비어있을 수 없습니다. 입력값: '{self.value}'"
            )

    @classmethod
    def of(cls, value: str) -> JackTrainerId:
        return cls(value=value.strip())

    def __str__(self) -> str:
        return self.value

        # domain/value_objects/passenger_name.py

from __future__ import annotations
from dataclasses import dataclass
from domain.exceptions.domain_exceptions import InvalidValueObjectError

_MIN_LENGTH = 1
_MAX_LENGTH = 100


@dataclass(frozen=True)
class PassengerName:
    """
    승객 이름 Value Object.
    - 최소 1자, 최대 100자
    - 앞뒤 공백 제거 후 저장
    """
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise InvalidValueObjectError("승객 이름은 비어있을 수 없습니다.")
        stripped = self.value.strip()
        if not (_MIN_LENGTH <= len(stripped) <= _MAX_LENGTH):
            raise InvalidValueObjectError(
                f"승객 이름은 {_MIN_LENGTH}~{_MAX_LENGTH}자 이내여야 합니다. "
                f"입력값 길이: {len(stripped)}"
            )
        # frozen이므로 object.__setattr__ 사용
        object.__setattr__(self, "value", stripped)

    @classmethod
    def of(cls, value: str) -> PassengerName:
        return cls(value=value)

    @property
    def last_name(self) -> str:
        """성(Last Name) 추출 — 'Last, First' 형식 기준"""
        parts = self.value.split(",")
        return parts[0].strip() if parts else self.value

    def __str__(self) -> str:
        return self.value

# domain/value_objects/gender.py

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from domain.exceptions.domain_exceptions import InvalidValueObjectError


class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Gender:
    """
    성별 Value Object.
    - 허용값: male / female / unknown
    - 대소문자 무관 입력 허용 후 정규화
    """
    gender_type: GenderType

    def __post_init__(self) -> None:
        if not isinstance(self.gender_type, GenderType):
            raise InvalidValueObjectError(
                f"유효하지 않은 GenderType입니다: {self.gender_type}"
            )

    @classmethod
    def of(cls, raw: str | None) -> Gender:
        if raw is None:
            return cls(gender_type=GenderType.UNKNOWN)
        normalized = raw.strip().lower()
        try:
            return cls(gender_type=GenderType(normalized))
        except ValueError:
            raise InvalidValueObjectError(
                f"성별 값이 유효하지 않습니다: '{raw}'. "
                f"허용값: {[e.value for e in GenderType]}"
            )

    @property
    def is_male(self) -> bool:
        return self.gender_type == GenderType.MALE

    @property
    def is_female(self) -> bool:
        return self.gender_type == GenderType.FEMALE

    @property
    def is_unknown(self) -> bool:
        return self.gender_type == GenderType.UNKNOWN

    def __str__(self) -> str:
        return self.gender_type.value

# domain/value_objects/age.py

from __future__ import annotations
from dataclasses import dataclass
from domain.exceptions.domain_exceptions import InvalidValueObjectError

_MIN_AGE = 0.0
_MAX_AGE = 150.0


@dataclass(frozen=True)
class Age:
    """
    나이 Value Object.
    - 0 이상 150 이하 실수
    - None 허용 (타이타닉 데이터 특성상 결측치 존재)
    """
    value: float | None

    def __post_init__(self) -> None:
        if self.value is not None:
            if not (_MIN_AGE <= self.value <= _MAX_AGE):
                raise InvalidValueObjectError(
                    f"나이는 {_MIN_AGE}~{_MAX_AGE} 범위여야 합니다. 입력값: {self.value}"
                )

    @classmethod
    def of(cls, raw: str | None) -> Age:
        if raw is None or raw.strip() == "":
            return cls(value=None)
        try:
            return cls(value=float(raw.strip()))
        except ValueError:
            raise InvalidValueObjectError(
                f"나이 값을 숫자로 변환할 수 없습니다: '{raw}'"
            )

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_minor(self) -> bool:
        """미성년자 여부 (18세 미만)"""
        return self.value is not None and self.value < 18.0

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else "Unknown"

# domain/value_objects/family_info.py

from __future__ import annotations
from dataclasses import dataclass
from domain.exceptions.domain_exceptions import InvalidValueObjectError


@dataclass(frozen=True)
class FamilyInfo:
    """
    탑승 가족 정보 Value Object.
    - sib_sp: 함께 탑승한 형제/배우자 수
    - parch: 함께 탑승한 부모/자녀 수
    - 두 값을 하나의 VO로 묶어 응집도 향상 (Cohesion)
    """
    sib_sp: int  # Siblings + Spouse
    parch: int   # Parents + Children

    def __post_init__(self) -> None:
        if self.sib_sp < 0:
            raise InvalidValueObjectError(
                f"sib_sp(형제/배우자 수)는 0 이상이어야 합니다. 입력값: {self.sib_sp}"
            )
        if self.parch < 0:
            raise InvalidValueObjectError(
                f"parch(부모/자녀 수)는 0 이상이어야 합니다. 입력값: {self.parch}"
            )

    @classmethod
    def of(cls, raw_sib_sp: str | None, raw_parch: str | None) -> FamilyInfo:
        try:
            sib_sp = int(raw_sib_sp.strip()) if raw_sib_sp else 0
        except ValueError:
            raise InvalidValueObjectError(
                f"sib_sp 값을 정수로 변환할 수 없습니다: '{raw_sib_sp}'"
            )
        try:
            parch = int(raw_parch.strip()) if raw_parch else 0
        except ValueError:
            raise InvalidValueObjectError(
                f"parch 값을 정수로 변환할 수 없습니다: '{raw_parch}'"
            )
        return cls(sib_sp=sib_sp, parch=parch)

    @property
    def total_family_size(self) -> int:
        """총 동반 가족 수 (본인 제외)"""
        return self.sib_sp + self.parch

    @property
    def is_alone(self) -> bool:
        """혼자 탑승 여부"""
        return self.total_family_size == 0

    def __str__(self) -> str:
        return f"SibSp={self.sib_sp}, Parch={self.parch}"

# domain/value_objects/survived_status.py

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from domain.exceptions.domain_exceptions import InvalidValueObjectError


class SurvivedType(str, Enum):
    SURVIVED = "1"
    NOT_SURVIVED = "0"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SurvivedStatus:
    """
    생존 여부 Value Object.
    - "1" = 생존, "0" = 사망, None = 미확인
    - 도메인 언어로 의미를 명확히 표현
    """
    status: SurvivedType

    def __post_init__(self) -> None:
        if not isinstance(self.status, SurvivedType):
            raise InvalidValueObjectError(
                f"유효하지 않은 SurvivedType입니다: {self.status}"
            )

    @classmethod
    def of(cls, raw: str | None) -> SurvivedStatus:
        if raw is None or raw.strip() == "":
            return cls(status=SurvivedType.UNKNOWN)
        normalized = raw.strip()
        try:
            return cls(status=SurvivedType(normalized))
        except ValueError:
            raise InvalidValueObjectError(
                f"생존 여부 값이 유효하지 않습니다: '{raw}'. "
                f"허용값: {[e.value for e in SurvivedType]}"
            )

    @property
    def is_survived(self) -> bool:
        return self.status == SurvivedType.SURVIVED

    @property
    def is_unknown(self) -> bool:
        return self.status == SurvivedType.UNKNOWN

    def __str__(self) -> str:
        return self.status.value

