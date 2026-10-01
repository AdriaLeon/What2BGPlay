import re

from app.lib.normalization import normalize_board_game_name
from app.models.board_game import BoardGame
from sqlalchemy.orm import Session
from dataclasses import dataclass
from app.models.genre import Genre


def is_within_one_edit(search: str, target: str) -> bool:
    if search == target:
        return True

    if abs(len(search) - len(target)) > 1:
        return False

    if len(search) == len(target):
        differences = sum(
            a != b
            for a, b in zip(search, target)
        )

        return differences <= 1

    if len(search) > len(target):
        search, target = target, search

    i = 0
    j = 0
    differences = 0

    while i < len(search) and j < len(target):
        if search[i] == target[j]:
            i += 1
            j += 1
        else:
            differences += 1
            j += 1

            if differences > 1:
                return False

    return True


def matches_game_name(
    search_name: str,
    normalized_title: str,
) -> bool:
    if not search_name:
        return True

    # Exact/partial match
    if search_name in normalized_title:
        return True

    search_length = len(search_name)

    for start in range(len(normalized_title)):
        for length in (
            search_length - 1,
            search_length,
            search_length + 1,
        ):
            if length <= 0:
                continue

            end = start + length

            if end > len(normalized_title):
                continue

            candidate = normalized_title[start:end]

            if is_within_one_edit(
                search_name,
                candidate,
            ):
                return True

    return False


def filter_games_by_name(
games: list[BoardGame],
    name: str | None,
) -> list[BoardGame]:
    
    if not name:
        return games

    normalized_name = normalize_board_game_name(name)

    if not normalized_name:
        return games

    return [
        game
        for game in games
        if matches_game_name(
            normalized_name,
            game.normalized_title,
        )
    ]


def search_games(
    db: Session,
    min_players: int | None = None,
    max_players: int | None = None,
    name: str | None = None,
    duration: int | None = None,
    genre: str | None = None,
) -> list[BoardGame]:
    
    query = db.query(BoardGame)

    if min_players is not None:
        query = query.filter(
            BoardGame.max_players >= min_players,
        )

    if max_players is not None:
        query = query.filter(
            BoardGame.min_players <= max_players,
        )

    if duration is not None:
        query = query.filter(
            BoardGame.duration_minutes <= duration,
        )

    if genre is not None:
        query = (
            query
            .join(BoardGame.genres)
            .filter(Genre.name == genre)
        )

    games = (
        query
        .order_by(BoardGame.title)
        .all()
    )

    return filter_games_by_name(
        games,
        name,
    )