"""
Deck initialization and modification.

This module contains functions for creating and shuffling a deck of cards.
"""

__author__ = 'Adrien P.'

import random

from card import Card
from constants import CARD_RANKS, CARD_SUITS

def create_deck() -> list[Card]:
    """
    Create and return a 52 card deck.

    Returns:
        list[Card]: The deck of cards.
    """
    return [Card(suit, rank) for suit in CARD_SUITS for rank in CARD_RANKS]

def shuffle_deck(deck: list[Card]) -> list[Card]:
    """
    Shuffle and return the deck of cards.

    Args:
        deck (list[Card]): The deck to shuffle.

    Returns:
        list[Card]: The deck of cards.
    """
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]
    return deck
