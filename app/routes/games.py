from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.board_game import BoardGame
from app.models.genre import Genre
from app.models.image import BoardGameImage
from app.schemas.board_game import BoardGameCreate, BoardGameResponse
from app.services.auth.dependencies import get_current_user
from app.models.user import User, UserBoardGame
from app.lib.normalization import normalize_board_game_name


router = APIRouter(
    prefix="/games",
    tags=["Board Games"],
)

# Used to map to genres and images into a str array to satisfy the API schema
def to_board_game_response(game: BoardGame) -> BoardGameResponse:
    return BoardGameResponse(
        id=game.id,
        title=game.title,
        min_players=game.min_players,
        max_players=game.max_players,
        duration_minutes=game.duration_minutes,
        description=game.description,
        genres=[genre.name for genre in game.genres],
        images=[image.image_url for image in game.images],
        created_at=game.created_at,
    )


@router.post(
    "",
    response_model=BoardGameResponse,
    status_code=201,
)
def create_game(
    game: BoardGameCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Find existing genres or create new ones
    genres = []

    for genre_name in game.genres:
        genre = (
            db.query(Genre)
            .filter(Genre.name == genre_name)
            .first()
        )

        if genre is None:
            genre = Genre(name=genre_name)
            db.add(genre)

        genres.append(genre)

    # Create the board game
    db_game = BoardGame(
        title=game.title,
        normalized_title=normalize_board_game_name(game.title),
        min_players=game.min_players,
        max_players=game.max_players,
        duration_minutes=game.duration_minutes,
        description=game.description,
        genres=genres,
    )

    # Add images
    for image_url in game.images:
        db_game.images.append(
            BoardGameImage(image_url=image_url)
        )

    db.add(db_game)

    # Flush so db_game.id is generated before creating the association
    db.flush()

    # Automatically add the new game to the creator's collection
    user_game = UserBoardGame(
        user_id=current_user.id,
        board_game_id=db_game.id,
    )

    db.add(user_game)

    # Commit everything together
    db.commit()
    db.refresh(db_game)

    return to_board_game_response(db_game)


@router.get(
    "",
    response_model=list[BoardGameResponse],
)
def get_games(
    db: Session = Depends(get_db),
):
    games = db.query(BoardGame).all()

    return [
        to_board_game_response(game)
        for game in games
    ]

@router.get(
    "/recommend",
    response_model=BoardGameResponse,
)
def recommend_game(
    players: int | None = Query(default=None, ge=1),
    genre: str | None = Query(default=None),
    max_time: int | None = Query(default=None, ge=1),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = (
        db.query(BoardGame)
        .join(
            UserBoardGame,
            UserBoardGame.board_game_id == BoardGame.id,
        )
        .filter(
            UserBoardGame.user_id == current_user.id,
        )
    )

    if players is not None:
        query = query.filter(
            BoardGame.min_players <= players,
            BoardGame.max_players >= players,
        )

    if genre is not None:
        query = query.join(BoardGame.genres).filter(
            Genre.name == genre,
        )

    if max_time is not None:
        query = query.filter(
            BoardGame.duration_minutes <= max_time,
        )

    games = (
        query
        .order_by(BoardGame.id)
        .distinct()
        .all()
    )

    if not games:
        raise HTTPException(
            status_code=404,
            detail="No games in your collection match the selected filters",
        )

    game = games[offset % len(games)]

    return to_board_game_response(game)

@router.get(
    "/search",
    response_model=list[BoardGameResponse],
)
def search_games(
    min_players: int | None = Query(default=None, ge=1),
    max_players: int | None = Query(default=None, ge=1),
    name: str | None = Query(default=None),
    duration: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
):
    query = db.query(BoardGame)

    if min_players is not None:
        query = query.filter(
            BoardGame.max_players >= min_players,
        )

    if max_players is not None:
        query = query.filter(
            BoardGame.min_players <= max_players,
        )

    if name is not None:
        normalized_name = normalize_board_game_name(name)

        query = query.filter(
            BoardGame.normalized_title.contains(normalized_name),
        )

    if duration is not None:
        query = query.filter(
            BoardGame.duration_minutes <= duration,
        )

    games = (
        query
        .order_by(BoardGame.title)
        .all()
    )

    return [
        to_board_game_response(game)
        for game in games
    ]

@router.get(
    "/{game_id}",
    response_model=BoardGameResponse,
)
def get_game(
    game_id: int,
    db: Session = Depends(get_db),
):
    game = db.get(BoardGame, game_id)

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Board game not found",
        )

    return to_board_game_response(game)


@router.delete(
    "/{game_id}",
    status_code=204,
)
def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
):
    game = db.get(BoardGame, game_id)

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Board game not found",
        )

    db.delete(game)
    db.commit()