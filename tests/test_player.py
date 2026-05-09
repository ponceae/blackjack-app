"""
Tests for the `player.py` module.
"""

__author__ = 'Adrien P.'

import pytest
from typing import Any

from entities.bank import Bank
from entities.card import Card
from entities.hand import Hand
from entities.player import Player, PlayerHand

def _generate_player_objects():
    """Provide a list of `Player` objects."""
    return [
        Player(
            bank=Bank(15.0), 
            hands=[
                PlayerHand(cards=[Card('Hearts', 5), Card('Spades', 4)]), 
            ],
        ),
        Player(
            bank=Bank(100.5), 
            hands=[
                PlayerHand(cards=[Card('Clubs', 'Ace'), Card('Diamonds', 10)]), 
            ],
        ),
        Player(
            bank=Bank(150.25), 
            hands=[
                PlayerHand(cards=[Card('Hearts', 10), Card('Spades', 2)]),
                PlayerHand(cards=[Card('Diamonds', 9), Card('Clubs', 'Jack')]),
            ],
        ),
        Player(
            bank=Bank(250.0), 
            hands=[
                PlayerHand(cards=[Card('Diamonds', 'Queen'), Card('Clubs', 'King')]),
            ],
        ),
        Player(
            bank=Bank(500.0), 
            hands=[
                PlayerHand(cards=[Card('Diamonds', 3), Card('Spades', 2)]),
                PlayerHand(cards=[Card('Spades', 7), Card('Clubs', 'Jack')]),
            ],
        ),
    ]

def _player_mapping_pairs():
    """
    Generate pairs of `Player` instances and their expected {`bank`, `hands`} dicts.
    """
    return [
        (player, {'bank': player.bank.to_dict(), 'hands': [hand.to_dict() for hand in player.hands]})
        for player in _generate_player_objects()
    ]

@pytest.fixture
def player():
    return Player()

def test_player_default_factory_creates_moderate_bank_and_empty_list(player):
    assert player.bank.balance == 500.0
    assert len(player.hands) == 0

# ===========================================
# Player Serialization/Deserialization Tests.
# ===========================================

@pytest.mark.parametrize(
    'expected_player, data_dict',
    _player_mapping_pairs()
)
def test_from_dict_creates_player_instance(expected_player, data_dict):
    test_player = Player.from_dict(data_dict)

    assert test_player.bank == expected_player.bank
    assert test_player.hands == expected_player.hands

@pytest.mark.parametrize(
    'player, expected_data_dict',
    _player_mapping_pairs()
)
def test_to_dict_creates_correct_data(player, expected_data_dict):
    data_dict = player.to_dict()

    assert data_dict == expected_data_dict
