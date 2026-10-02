from fastapi import FastAPI

from app.database import Base, engine
from app.routes.games import router as games_router
from app.routes.users import router as users_router
from app.routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

from app.models.board_game import BoardGame, BoardGameGenre
from app.models.user import User, UserBoardGame

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="What2BGPlay",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(games_router)
app.include_router(auth_router)