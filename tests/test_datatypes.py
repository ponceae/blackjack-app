""" 
Tests for the `datatypes.py` module.
"""

import pytest

from card import Card
from datatypes import Hand

# ============
# Hand Tests.
# ============
def _two_card_hand_serialization_mapping() -> list[tuple]:
    """Provide a list of mapped packed and unpacked `Hand` objects."""
    return [
        (
            Hand(value=11, cards=[Card('Clubs', 5), Card('Spades', 6)]), 
            {
                'value': 11, 
                'cards': [{'suit': 'Clubs', 'rank': 5}, {'suit': 'Spades', 'rank': 6}]
            }
        ),
    ]

@pytest.mark.parametrize(
    'expected_hand, data_dict',
    _two_card_hand_serialization_mapping(),
)
def test_hand_from_dict_creates_object(expected_hand, data_dict):
    test_hand = Hand.from_dict(data_dict)
    
    assert test_hand.value == expected_hand.value
    
    assert len(test_hand.cards) == 2
    assert test_hand.cards[0].rank == expected_hand.cards[0].rank
    assert test_hand.cards[0].suit == expected_hand.cards[0].suit
    
    assert test_hand.cards[1].rank == expected_hand.cards[1].rank
    assert test_hand.cards[1].suit == expected_hand.cards[1].suit

def test_hand_to_dict_creates_data_dict():
    pass
