import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base


TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def create_test_database():
    Base.metadata.create_all(bind=engine)


def drop_test_database():
    Base.metadata.drop_all(bind=engine)