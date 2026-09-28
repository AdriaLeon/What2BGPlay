from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.board_game import BoardGame
from app.models.user import User, UserBoardGame
from app.schemas.user import (UserGameCreate,UserGameResponse,UserResponse,)
from app.services.auth.dependencies import get_current_user
from app.models.genre import Genre
from app.models.image import BoardGameImage

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get(    
    "/me/games",
    response_model=list[UserGameResponse],
)
def get_my_games(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    statement = (
        select(BoardGame)
        .join(UserBoardGame)
        .where(UserBoardGame.user_id == current_user.id)
    )

    return db.scalars(statement).all()

@router.post(
    "/me/games",
    response_model=UserGameResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_game(
    data: UserGameCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Try to find existing game
    game = None

    if data.board_game_id is not None:
        game = db.get(BoardGame, data.board_game_id)

    # If game doesn't exist, create it
    if game is None:

        # These fields are required to create a new game
        if (
            data.title is None
            or data.min_players is None
            or data.max_players is None
            or data.duration_minutes is None
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "title, min_players, max_players and "
                    "duration_minutes are required when creating a game"
                ),
            )

        # Find or create genres
        genres = []

        for genre_name in data.genres:
            genre = db.scalar(
                select(Genre).where(Genre.name == genre_name)
            )

            if genre is None:
                genre = Genre(name=genre_name)
                db.add(genre)

            genres.append(genre)

        # Create board game
        game = BoardGame(
            title=data.title,
            min_players=data.min_players,
            max_players=data.max_players,
            duration_minutes=data.duration_minutes,
            description=data.description,
            genres=genres,
        )

        # Add images
        for image_url in data.images:
            game.images.append(
                BoardGameImage(image_url=image_url)
            )

        db.add(game)

        # Get generated ID before creating UserBoardGame
        db.flush()

    # Check if user already has this game
    existing = db.scalar(
        select(UserBoardGame).where(
            UserBoardGame.user_id == current_user.id,
            UserBoardGame.board_game_id == game.id,
        )
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Board game is already in your collection",
        )

    # Add game to user's collection
    user_game = UserBoardGame(
        user_id=current_user.id,
        board_game_id=game.id,
    )

    db.add(user_game)

    db.commit()
    db.refresh(game)

    return game

@router.delete(
    "/me/games/{board_game_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_game(
    board_game_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_game = db.scalar(
        select(UserBoardGame).where(
            UserBoardGame.user_id == current_user.id,
            UserBoardGame.board_game_id == board_game_id,
        )
    )

    if user_game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board game is not in your collection",
        )

    db.delete(user_game)
    db.commit()