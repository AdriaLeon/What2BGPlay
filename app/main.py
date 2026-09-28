from fastapi import FastAPI

from app.database import Base, engine
from app.routes.games import router as games_router

from app.models.board_game import BoardGame


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="What2BGPlay",
    version="0.1.0",
)


app.include_router(games_router)