from types import SimpleNamespace

from app.lib.game_search import (
    is_within_one_edit,
    matches_game_name,
    filter_games_by_name,
)


def test_exact_name_match():
    assert is_within_one_edit("catan", "catan")


def test_single_character_substitution():
    assert is_within_one_edit("ca7an", "catan")


def test_single_character_insertion():
    assert is_within_one_edit("catann", "catan")


def test_single_character_deletion():
    assert is_within_one_edit("cata", "catan")


def test_two_edits_do_not_match():
    assert not is_within_one_edit("ca7bn", "catan")

def test_partial_name_match():
    assert matches_game_name("catan","catan5thedition")


def test_fuzzy_partial_name_match():
    assert matches_game_name("ca7an","catan5thedition")


def test_unrelated_name_does_not_match():
    assert not matches_game_name("monopoly","catan5thedition")