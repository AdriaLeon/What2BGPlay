from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BoardGameImage(Base):
    __tablename__ = "board_game_images"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    board_game_id: Mapped[int] = mapped_column(
        ForeignKey("board_games.id", ondelete="CASCADE"),
        nullable=False,
    )

    image_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    board_game: Mapped["BoardGame"] = relationship(
        back_populates="images",
    )