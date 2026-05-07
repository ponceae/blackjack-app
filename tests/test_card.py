"""
Tests for the `card.py` module.

Ensures the `Card` class correctly initializes and validates the suit name, the rank
value or name, and validates object packing and unpacking.
"""

__author__ = 'Adrien P.'

import pytest
from typing import Any

from constants import CARD_RANKS, CARD_SUITS
from data.constants import CARD_INVALID_RANK_ERR_MSG, CARD_INVALID_SUIT_ERR_MSG
from entities.card import Card

# =========================
# Card and Map Generators.
# =========================

def _generate_card_test_data() -> list[tuple[Card, int, str, str]]:
    """Provide a list of `Card` test data"""
    return [
        (Card('Spades', 5), 5, '♠5', "Card(suit='Spades', rank='5')"),
        (Card('Hearts', 2), 2, '♥2', "Card(suit='Hearts', rank='2')"),
        (Card('Clubs', 10), 10, '♣10', "Card(suit='Clubs', rank='10')"),
        (Card('Diamonds', 'Ace'), 11, '♦Ace', "Card(suit='Diamonds', rank='Ace')"),
        (Card('Spades', 'Jack'), 10, '♠Jack', "Card(suit='Spades', rank='Jack')"),
        (Card('Clubs', 'Queen'), 10, '♣Queen', "Card(suit='Clubs', rank='Queen')"),
        (Card('Hearts', 'King'), 10, '♥King', "Card(suit='Hearts', rank='King')"),
    ]

def _card_mapping_pairs() -> list[tuple[Card, dict[str, Any]]]:
    """
    Generate pairs of `Card` instances and their expected {`suit`, `rank`} dicts.
    """
    return [
        (card, {'suit': card.suit, 'rank': card.rank}) 
        for (card, *_) in _generate_card_test_data()
    ]

# ==========================
# Card Initialization Tests.
# ==========================

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
    test_card = Card(raw_suit, raw_rank)
    expected_card = Card(exp_suit, exp_rank)
    
    assert test_card == expected_card
    
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
    'inv_suit, inv_rank, exp_err_msg',
    [
        (5, 8, CARD_INVALID_SUIT_ERR_MSG),
        ('Card', 'Ace', CARD_INVALID_SUIT_ERR_MSG),
        ('Spades', '5', CARD_INVALID_RANK_ERR_MSG),
        ('Hearts', 12, CARD_INVALID_RANK_ERR_MSG),
        ('Diamonds', 1, CARD_INVALID_RANK_ERR_MSG),   
    ],
    ids=[
        'invalid_suit_a_int',
        'invalid_suit_b_err',
        'invalid_rank_a_str',
        'invalid_rank_b_big',
        'invalid_rank_c_small',
    ],
)
def test_init_raises_valueerror_on_invalid_input(inv_suit, inv_rank, exp_err_msg,):
    with pytest.raises(ValueError, match=exp_err_msg):
        Card(inv_suit, inv_rank)

# =========================
# Card Dunder Method Tests.
# =========================

def test_card_equality():
    card1 = Card('Spades', 5)
    card2 = Card('Spades', 5)
    card3 = Card('Diamonds', 6)
    
    assert card1 == card2
    
    assert card1 != card3
    
    assert card1 != '5 of Spades'

@pytest.mark.parametrize(
    'card, expected_rank_value',
    [(card, value) for (card, value, *_) in _generate_card_test_data()]
)
def test_card_rank_value(card, expected_rank_value):
    assert card.rank_value == expected_rank_value

@pytest.mark.parametrize(
    'card, expected_string',
    [(card, string) for (card, _, string, *_) in _generate_card_test_data()],
)
def test_card_string_display(card, expected_string):
    assert str(card) == expected_string

@pytest.mark.parametrize(
    'card, expected_string',
    [(card, string) for (card, *_, string) in _generate_card_test_data()],
)
def test_card_debug_display(card, expected_string):
    assert repr(card) == expected_string

# =========================================
# Card Serialization/Deserialization Tests.
# =========================================

@pytest.mark.parametrize('expected_card, data_dict', _card_mapping_pairs())
def test_from_dict_creates_card_instance(expected_card, data_dict):
    test_card = Card.from_dict(data_dict)
    
    assert test_card.suit == expected_card.suit
    assert test_card.rank == expected_card.rank

@pytest.mark.parametrize('card, expected_data_dict', _card_mapping_pairs())
def test_to_dict_creates_correct_data(card, expected_data_dict):
    data_dict = card.to_dict()
    
    assert data_dict == expected_data_dict
