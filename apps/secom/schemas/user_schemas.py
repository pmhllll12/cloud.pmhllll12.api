from pydantic import BaseModel, Field


class UserSchemas(BaseModel):
    user_id: str = Field(..., min_length=2, max_length=64)
    email: str
    nickname: str = Field(..., min_length=1, max_length=64)
    phone: str = Field(..., min_length=9, max_length=32)
    password: str
    password_confirm: str
    role: str
