"""
Describes and visualizes a single playing card.

This module provides the `Card` class, which represents a single playing card from 
a deck, and determines its numeric value.
"""

__author__ = 'Adrien P.'

from .constants import (
    ACE,
    CARD_SUITS, 
    CARD_SUIT_SYMBOLS, 
    DEFAULT_ACE_VALUE, 
    FACE_CARD_VALUE, 
    NAMED_CARD_RANKS,
)

class Card:
    """
     Represents a single playing card with a rank and suit.

       Attributes:
        suit (str): The card's suit name.
        rank (int | str): The card's rank (an integer for pip cards, or a string for
              face cards and Aces).
    """

    def __init__ (self, suit: str, rank: int | str) -> None:
        """
        Initialize a `Card` with the given suit and rank.

        Args:
            suit (str): The suit name to give to the card
                (`'Clubs'`, `'Diamonds'`, `'Hearts'`, `'Spades'`).
            rank (int | str): The rank to give to the card
                (`2` through `10`, `'Jack'`, `'Queen'`, `'King'`, `'Ace'`).

        Raises:
            ValueError: If an invalid suit name is entered (name that does not exist)
            or an invalid rank is entered (outside of bounds or rank name does
            not exist).
        """
        if isinstance(suit, str) and suit.capitalize() in CARD_SUITS:
            self.suit = suit.capitalize()
        else:
            raise ValueError(
                f'Invalid suit, `suit` must be one of: '
                f'\'Clubs\', \'Diamonds\', \'Hearts\', \'Spades\'.'
              )

        if isinstance(rank, int) and (2 <= rank <= 11):
            self.rank = rank
        elif isinstance(rank, str) and rank.capitalize() in NAMED_CARD_RANKS:
            self.rank = rank.capitalize()
        else:
            raise ValueError(
                f'Invalid rank, `rank` must be one of: '
                f'\'2\' through \'10\', \'Jack\', \'King\', \'Queen\', \'Ace\'.'
            )

    def get_rank_value(self) -> int:
        """
        Return the rank value of the `Card`. If the rank value is an Ace, return a 
        value of `11`. If the rank value is a face card, return a value of `10`.

        Returns:
            int: The rank value.
        """
        if isinstance(self.rank, int):
            return self.rank
        elif isinstance(self.rank, str):
            if self.rank != ACE:
                return FACE_CARD_VALUE
            else:
                return DEFAULT_ACE_VALUE

        return 0

    def to_string(self) -> str:
        """
        Return the string representation of the `Card`.

        Returns:
            str: The string representation (e.g., ♦5).
        """
        return f'{CARD_SUIT_SYMBOLS[self.suit]}{str(self.rank)}'
