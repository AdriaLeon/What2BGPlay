from pydantic import BaseModel, EmailStr, ConfigDict

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

class UserGameResponse(BaseModel):
    id: int
    title: str
    min_players: int
    max_players: int
    duration_minutes: int

    model_config = ConfigDict(from_attributes=True)

class UserGameCreate(BaseModel):
    board_game_id: int