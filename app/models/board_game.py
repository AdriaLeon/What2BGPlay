from app.database import Base
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class BoardGame(Base):
    __tablename__ = "board_games"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    min_players: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    max_players: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    genres: Mapped[list["Genre"]] = relationship(
        secondary="board_game_genres",
        back_populates="board_games",
    )

    images: Mapped[list["BoardGameImage"]] = relationship(
        back_populates="board_game",
        cascade="all, delete-orphan",
    )

    users: Mapped[list["UserBoardGame"]] = relationship(
    back_populates="board_game",
    cascade="all, delete-orphan",
    )

class BoardGameGenre(Base):
    __tablename__ = "board_game_genres"

    board_game_id: Mapped[int] = mapped_column(
        ForeignKey("board_games.id", ondelete="CASCADE"),
        primary_key=True,
    )

    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.id", ondelete="CASCADE"),
        primary_key=True,
    )