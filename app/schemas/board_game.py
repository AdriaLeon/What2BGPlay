from datetime import datetime

from pydantic import BaseModel, Field

class BoardGameCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    min_players: int = Field(ge=1)
    max_players: int = Field(ge=1)
    duration_minutes: int = Field(gt=0)
    description: str | None = None

    genres: list[str] = Field(default_factory=list)
    images: list[str] = Field(default_factory=list)


class BoardGameResponse(BaseModel):
    id: int
    title: str
    min_players: int
    max_players: int
    duration_minutes: int
    description: str | None
    genres: list[str]
    images: list[str]
    created_at: datetime