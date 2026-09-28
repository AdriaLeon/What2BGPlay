from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import UserResponse
from app.services.auth.dependencies import get_current_user
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.board_game import BoardGame
from app.models.board_game import UserBoardGame
from app.schemas.user import UserGameResponse, UserGameCreate


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get("/me/games", response_model=list[UserGameResponse])
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
    status_code=201,
)
def add_game(
    data: UserGameCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    game = db.get(BoardGame, data.board_game_id)

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Board game not found",
        )

    user_game = UserBoardGame(
        user_id=current_user.id,
        board_game_id=game.id,
    )

    db.add(user_game)
    db.commit()

    return game