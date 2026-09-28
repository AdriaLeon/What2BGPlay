from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class GenreResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ImageResponse(BaseModel):
    id: int
    image_url: str

    model_config = ConfigDict(from_attributes=True)


class UserGameResponse(BaseModel):
    id: int
    title: str
    min_players: int
    max_players: int
    duration_minutes: int
    description: str | None = None

    genres: list[GenreResponse] = Field(default_factory=list)
    images: list[ImageResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class UserGameCreate(BaseModel):
    board_game_id: int | None = None
    title: str | None = None
    min_players: int | None = None
    max_players: int | None = None
    duration_minutes: int | None = None
    description: str | None = None
    genres: list[str] = Field(default_factory=list)
    images: list[str] = Field(default_factory=list)