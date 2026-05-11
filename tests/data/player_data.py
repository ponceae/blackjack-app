""" 
Test generator and mapping logic for the `test_player.py` module.

Provides:
    - Player object generator.
    - Dictionary factory for `from_dict`/`to_dict`.
"""

__author__ = 'Adrien P.'

from typing import Any

from entities.bank import Bank
from entities.card import Card
from entities.hand import PlayerHand
from entities.player import Player

def generate_player_objects() -> list[Player]:
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

def player_mapping_pairs() -> list[tuple[Player, dict[str, Any]]]:
    """
    Generate pairs of `Player` instances and their expected {`bank`, `hands`} dicts.
    """
    return [
        (player, {
            'bank': player.bank.to_dict(), 
            'hands': [hand.to_dict() for hand in player.hands]
            }
        )
        for player in generate_player_objects()
    ]
