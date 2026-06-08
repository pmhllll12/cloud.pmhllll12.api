from pydantic import BaseModel, Field


class WalterRoasterSchema(BaseModel):
    id: int = Field(default=1, description="식별자")
    name: str = Field(default="Walter", description="이름")
    memo: str = Field(
        default="월터는 타이타닉의 승무원이다",
        description="메모",
    )
