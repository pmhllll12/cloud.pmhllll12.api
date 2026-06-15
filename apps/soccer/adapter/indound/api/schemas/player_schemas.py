from typing import Optional

from pydantic import BaseModel, Field


class PlayerSchema(BaseModel):
    id: int = Field(0, description="Player ID (FK → PERSONS.id)")
    position: Optional[str] = Field(None, description="Position: FW | MF | DF | GK")
    jersey_number: Optional[int] = Field(None, description="Jersey number")
    team_id: Optional[int] = Field(None, description="Team ID (FK → TEAMS.id)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "position": "FW",
                "jersey_number": 7,
                "team_id": 3,
            }
        }
    }


class PlayerCreateSchema(BaseModel):
    id: int = Field(..., description="PERSONS.id")
    position: Optional[str] = Field(None, max_length=10)
    jersey_number: Optional[int] = Field(None, ge=1, le=99)
    team_id: Optional[int] = None


