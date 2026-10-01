import app.models

import pytest

from app.database import SessionLocal
from app.models.board_game import BoardGame
from app.models.genre import Genre
from tests.database import TestingSessionLocal, create_test_database, drop_test_database

@pytest.fixture(scope="session", autouse=True)
def test_database():
    create_test_database()

    yield

    drop_test_database()


@pytest.fixture
def db():
    db = TestingSessionLocal()

    try:
        strategy = Genre(name="strategy")

        game = BoardGame(
            title="Catan",
            normalized_title="catan",
            min_players=3,
            max_players=4,
            duration_minutes=60,
            description="A strategy game.",
            genres=[strategy],
        )

        db.add_all([strategy, game])
        db.commit()

        yield db

    finally:
        db.rollback()

        # Clean data created by this test
        db.query(BoardGame).delete()
        db.query(Genre).delete()

        db.commit()
        db.close()