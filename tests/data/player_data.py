""" 
Test generator and mapping logic for the `test_player.py` module.

Provides:
    - Player object generator.
    - Dictionary factory for `from_dict`/`to_dict`.
"""

__author__ = 'Adrien P.'

from typing import Any

from entities import Bank, Card, PlayerHand, Player

def _generate_player_objects() -> list[Player]:
    """Provide a list of `Player` objects."""
    return [
        Player(
            bank=Bank(15.0), 
            hands=[
                PlayerHand(cards=[Card('Hearts', 5), Card('Spades', 4)]), 
            ],
            active_hand_index=0,
        ),
        Player(
            bank=Bank(100.5), 
            hands=[
                PlayerHand(cards=[Card('Clubs', 'Ace'), Card('Diamonds', 10)]), 
            ],
            active_hand_index=0,
        ),
        Player(
            bank=Bank(150.25), 
            hands=[
                PlayerHand(cards=[Card('Hearts', 10), Card('Spades', 2)]),
                PlayerHand(cards=[Card('Diamonds', 9), Card('Clubs', 'Jack')]),
            ],
            active_hand_index=1,
        ),
        Player(
            bank=Bank(250.0), 
            hands=[
                PlayerHand(cards=[Card('Diamonds', 'Queen'), Card('Clubs', 'King')]),
            ],
            active_hand_index=0,
        ),
        Player(
            bank=Bank(500.0), 
            hands=[
                PlayerHand(cards=[Card('Diamonds', 3), Card('Spades', 2)]),
                PlayerHand(cards=[Card('Spades', 7), Card('Clubs', 'Jack')]),
            ],
            active_hand_index=1,
        ),
    ]

def player_mapping_pairs() -> list[tuple[Player, dict[str, Any]]]:
    """
    Generate pairs of `Player` instances and their expected 
    {'bank', 'hands', 'active_hand_index'} dicts.
    """    
    return [
        (player, {
            'bank': player.bank.to_dict(), 
            'hands': [hand.to_dict() for hand in player.hands],
            'active_hand_index': player.active_hand_index
            }
        )
        for player in _generate_player_objects()
    ]
