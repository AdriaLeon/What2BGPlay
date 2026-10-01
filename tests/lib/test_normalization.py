from app.lib.normalization import normalize_board_game_name


def test_normalize_removes_spaces():
    assert normalize_board_game_name("Ca Tan") == "catan"


def test_normalize_removes_special_characters():
    assert normalize_board_game_name("Catan: 5th Edition") == "catan5thedition"


def test_normalize_accents():
    assert normalize_board_game_name("Café") == "cafe"