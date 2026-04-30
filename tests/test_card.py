"""
Tests for the `card.py` module.

Ensures the `Card` class correctly initializes and validates the suit name and the 
rank value or name.
"""

__author__ = 'Adrien P.'

import pytest

from card import Card
from constants import CARD_RANKS, CARD_SUITS
from data.constants import CARD_INVALID_RANK_ERR_MSG, CARD_INVALID_SUIT_ERR_MSG

@pytest.mark.parametrize(
    'raw_suit, raw_rank, exp_suit, exp_rank',
    [
        ('spaDEs', 5, 'Spades', 5),
        ('heArTs', 2, 'Hearts', 2),
        ('CLUbs', 10, 'Clubs', 10),
        ('DiaMONds', 'acE', 'Diamonds', 'Ace'),
        ('SPadEs', 'jaCk', 'Spades', 'Jack'),
        ('HEArtS', 'queen', 'Hearts', 'Queen'),
    ],
)
def test_init_mismatch_conversion(raw_suit, raw_rank, exp_suit, exp_rank):
    card = Card(raw_suit, raw_rank)

    assert card.suit == exp_suit
    assert card.rank == exp_rank

@pytest.mark.parametrize(
    'expected_rank, expected_suit',
    [
        (rank, suit) for rank in CARD_RANKS for suit in CARD_SUITS
    ],
)
def test_all_cards_have_correct_rank_and_suit(expected_rank, expected_suit):
    card = Card(expected_suit, expected_rank)

    assert card.rank == expected_rank
    assert card.suit == expected_suit

@pytest.mark.parametrize(
    'invalid_suit, invalid_rank, expected_err_msg',
    [
        (5, 8, CARD_INVALID_SUIT_ERR_MSG),
        ('Spades', '5', CARD_INVALID_RANK_ERR_MSG),
        ('Hearts', 12, CARD_INVALID_RANK_ERR_MSG),
        ('Diamonds', 1, CARD_INVALID_RANK_ERR_MSG),
        ('Card', 'Ace', CARD_INVALID_SUIT_ERR_MSG),
    ],
    ids=[
        'invalid_suit_a_int',
        'invalid_rank_a_string',
        'invalid_rank_b_big',
        'invalid_rank_c_small',
        'invalid_suit_b_err',
    ],
)
def test_init_raises_valueerror_on_invalid_input(
    invalid_suit,
    invalid_rank,
    expected_err_msg
):
    with pytest.raises(ValueError, match=expected_err_msg):
        Card(invalid_suit, invalid_rank)

def _generate_cards() -> list[Card]:
    """Provide a list of `Card` objects in order to test their attributes."""
    return [
        Card('Spades', 5),
        Card('Hearts', 2),
        Card('Clubs', 10),
        Card('Diamonds', 'Ace'),
        Card('Spades', 'Jack'),
        Card('Clubs', 'Queen'),
        Card('Hearts', 'King'),
    ]

def _generate_expected_values(type) -> list[int | str]:
    """Provide a list of expected values for the `_generate_cards()` function."""
    if type == 'rank_values':
        return [5, 2, 10, 11, 10, 10, 10]
    elif type == 'to_string':
        return ['♠5', '♥2', '♣10', '♦Ace', '♠Jack', '♣Queen','♥King']
    return []

@pytest.mark.parametrize(
    'card, expected_rank_value',
    zip(_generate_cards(), _generate_expected_values('rank_values'))
)
def test_get_card_rank_value(card, expected_rank_value):
    assert card.get_rank_value() == expected_rank_value

@pytest.mark.parametrize(
    'card, expected_string',
    zip(_generate_cards(), _generate_expected_values('to_string'))
)
def test_card_to_string(card, expected_string):
    assert card.to_string() == expected_string
