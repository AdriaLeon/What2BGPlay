import re
import unicodedata


def normalize_board_game_name(name: str) -> str:
    name = unicodedata.normalize("NFKD", name)

    name = name.encode(
        "ascii",
        "ignore",
    ).decode("ascii")

    name = name.lower()

    name = re.sub(
        r"[^a-z0-9]",
        "",
        name,
    )

    return name