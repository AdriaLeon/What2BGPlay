from app.lib.game_query import parse_game_query

def test_parse_player_count(db):
    filters = parse_game_query(db,"2 players catan")

    assert filters.min_players == 2


def test_parse_duration_minutes(db):
    filters = parse_game_query(db,"catan 60 minutes")

    assert filters.duration == 60

def test_parse_duration_hours(db):
    filters = parse_game_query(db,"catan 1 hour")

    assert filters.duration == 60


def test_parse_natural_language_query(db):
    filters = parse_game_query(db,"ca7an 2 players under 60 minutes")

    assert filters.name == "ca7an"
    assert filters.min_players == 2
    assert filters.duration == 60


def test_parse_unknown_words_are_ignored(db):
    filters = parse_game_query(db,"2p like catan")

    assert filters.min_players == 2
    assert filters.name == "catan"


def test_parse_strategy_query(db):
    filters = parse_game_query(db,"strateg 2 player game")

    assert filters.min_players == 2
    assert filters.genre == "strategy"