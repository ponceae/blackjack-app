""" 
Test data generator and mapping logic for the `test_card.py` module.

Provides:
    - Card set generators with rank value and string representations.
    - Dictionary factories for testing `from_dict`/`to_dict`.
"""

__author__ = 'Adrien P.'

from typing import Any

from entities import Card

def generate_card_test_data() -> list[tuple[Card, int, str, str]]:
    """
    Test data for the `Card` ranks and suits, and the card's string and debug string
    display for each tuple.
    
    (Card(), rank, str(), repr()).
    """
    return [
        (Card('Spades', 5), 5, '♠5', "Card(suit='Spades', rank='5')"),
        (Card('Hearts', 2), 2, '♥2', "Card(suit='Hearts', rank='2')"),
        (Card('Clubs', 10), 10, '♣10', "Card(suit='Clubs', rank='10')"),
        (Card('Diamonds', 'Ace'), 11, '♦Ace', "Card(suit='Diamonds', rank='Ace')"),
        (Card('Spades', 'Jack'), 10, '♠Jack', "Card(suit='Spades', rank='Jack')"),
        (Card('Clubs', 'Queen'), 10, '♣Queen', "Card(suit='Clubs', rank='Queen')"),
        (Card('Hearts', 'King'), 10, '♥King', "Card(suit='Hearts', rank='King')"),
    ]

def card_mapping_pairs() -> list[tuple[Card, dict[str, Any]]]:
    """
    Generate pairs of `Card` instances and their expected {`suit`, `rank`} dicts.
    """
    return [
        (card, {'suit': card.suit, 'rank': card.rank}) 
        for (card, *_) in generate_card_test_data()
    ]
