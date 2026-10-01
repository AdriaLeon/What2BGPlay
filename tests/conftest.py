import app.models

import pytest

from app.database import SessionLocal
from app.models.board_game import BoardGame
from app.models.genre import Genre

@pytest.fixture
def db():
    db = SessionLocal()

    try:
        strategy = db.query(Genre).filter(Genre.name == "strategy").first()

        if strategy is None:
            strategy = Genre(name="strategy")
            db.add(strategy)
            db.flush()

        game = BoardGame(
            title="Catan",
            normalized_title="catan",
            min_players=3,
            max_players=4,
            duration_minutes=60,
            description="A strategy game.",
            genres=[strategy],
        )

        db.add(game)
        db.commit()

        yield db

    finally:
        db.rollback()
        db.close()