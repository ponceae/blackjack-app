"""
Tests for the `card.py` module.

Ensures the `Card` class correctly initializes and validates the suit name, the rank
value or name, and validates object serialization and deserialization.
"""

__author__ = 'Adrien P.'

import pytest

from card import Card
from constants import CARD_RANKS, CARD_SUITS
from data.constants import CARD_INVALID_RANK_ERR_MSG, CARD_INVALID_SUIT_ERR_MSG

# ======================
# Initialization Tests.
# ======================

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
    expected_err_msg,
):
    with pytest.raises(ValueError, match=expected_err_msg):
        Card(invalid_suit, invalid_rank)

# =====================================
# Serialization/Deserialization Tests.
# =====================================

def _card_serialization_mapping() -> list[tuple]:
    """Provide a list of mapped packed and unpacked `Card` objects."""
    return [
        (Card('Spades', 8), {'suit': 'Spades', 'rank': 8}),
        (Card('Hearts', 'Ace'), {'suit': 'Hearts', 'rank': 'Ace'}),
        (Card('Diamonds', 'King'), {'suit': 'Diamonds', 'rank': 'King'}),
        (Card('Clubs', 'Queen'), {'suit': 'Clubs', 'rank': 'Queen'}),
        (Card('Spades', 'Jack'), {'suit': 'Spades', 'rank': 'Jack'}),
        (Card('Hearts', 10), {'suit': 'Hearts', 'rank': 10}),
        (Card('Clubs', 5), {'suit': 'Clubs', 'rank': 5}),
    ]

@pytest.mark.parametrize(
    'expected_card, data_dict',
    _card_serialization_mapping(),
)
def test_from_dict_creates_object(expected_card, data_dict):
    test_card = Card.from_dict(data_dict)
    
    assert test_card.suit == expected_card.suit
    assert test_card.rank == expected_card.rank

@pytest.mark.parametrize(
    'card_object, expected_data_dict',
    _card_serialization_mapping()
)
def test_to_dict_creates_data_dict(card_object, expected_data_dict):
    data = card_object.to_dict()
    
    assert data == expected_data_dict

# =======================
# Rank and String Tests.
# =======================

def _generate_cards() -> list[Card]:
    """Provide a list of `Card` objects."""
    return [
        Card('Spades', 5),
        Card('Hearts', 2),
        Card('Clubs', 10),
        Card('Diamonds', 'Ace'),
        Card('Spades', 'Jack'),
        Card('Clubs', 'Queen'),
        Card('Hearts', 'King'),
    ]

@pytest.mark.parametrize(
    'card, expected_rank_value',
    zip(_generate_cards(), [5, 2, 10, 11, 10, 10, 10])
)
def test_get_card_rank_value(card, expected_rank_value):
    assert card.get_rank_value() == expected_rank_value

@pytest.mark.parametrize(
    'card, expected_string',
    zip(_generate_cards(), ['♠5', '♥2', '♣10', '♦Ace', '♠Jack', '♣Queen','♥King'])
)
def test_card_to_string(card, expected_string):
    assert card.to_string() == expected_string
