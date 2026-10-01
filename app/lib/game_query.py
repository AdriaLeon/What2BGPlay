import re
from dataclasses import dataclass
from sqlalchemy.orm import Session
from app.models.genre import Genre
from app.lib.normalization import normalize_board_game_name
from app.lib.game_search import (is_within_one_edit,matches_game_name)
from app.models.board_game import BoardGame

@dataclass
class GameSearchFilters:
    min_players: int | None = None
    max_players: int | None = None
    name: str | None = None
    duration: int | None = None
    genre: str | None = None


def parse_player_count(query: str) -> tuple[int | None, str]:
    pattern = r"\b(\d+)\s*(?:players?|p)\b"

    match = re.search(pattern, query, re.IGNORECASE)

    if not match:
        return None, query

    players = int(match.group(1))

    cleaned_query = (
        query[:match.start()]
        + " "
        + query[match.end():]
    )

    return players, cleaned_query


def parse_genre(
    db: Session,
    query: str,
) -> tuple[str | None, str]:
    words = query.lower().split()

    genres = db.query(Genre).all()

    for genre in genres:
        normalized_genre = normalize_board_game_name(genre.name)

        for word in words:
            normalized_word = normalize_board_game_name(word)

            if not normalized_word:
                continue

            if normalized_word in normalized_genre:
                return genre.name, query.replace(word, "")

            if is_within_one_edit(
                normalized_word,
                normalized_genre,
            ):
                return genre.name, query.replace(word, "")

    return None, query

def parse_duration(query: str) -> tuple[int | None, str]:
    pattern = (
        r"\b"
        r"(?:(?:under|below|less\s+than|max(?:imum)?|up\s+to)\s*)?"
        r"(\d+(?:\.\d+)?)"
        r"\s*(hours?|hrs?|h|minutes?|mins?|m)"
        r"\b"
    )

    match = re.search(pattern, query, re.IGNORECASE)

    if not match:
        return None, query

    value = float(match.group(1))
    unit = match.group(2).lower()

    if unit.startswith(("hour", "hr")) or unit == "h":
        duration = round(value * 60)
    else:
        duration = round(value)

    cleaned_query = (
        query[:match.start()]
        + " "
        + query[match.end():]
    )

    return duration, cleaned_query

def clean_search_name(
    db: Session,
    query: str,
) -> str | None:
    words = query.split()

    if not words:
        return None

    games = db.query(BoardGame).all()

    matched_words = []

    for word in words:
        normalized_word = normalize_board_game_name(word)

        if not normalized_word:
            continue

        if any(
            matches_game_name(
                normalized_word,
                game.normalized_title,
            )
            for game in games
        ):
            matched_words.append(word)

    if not matched_words:
        return None

    return " ".join(matched_words)

def parse_game_query(
    db: Session,
    query: str,
) -> GameSearchFilters:
    remaining_query = query.strip()

    players, remaining_query = parse_player_count(
        remaining_query,
    )

    genre, remaining_query = parse_genre(
        db,
        remaining_query,
    )

    duration, remaining_query = parse_duration(
        remaining_query,
    )

    name = clean_search_name(db, remaining_query)

    return GameSearchFilters(
        min_players=players,
        max_players=None,
        name=name,
        duration=duration,
        genre=genre,
    )