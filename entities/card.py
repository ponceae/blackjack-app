"""
Represents and validates a single playing card.

This module provides the `Card` class, which serves as the core building block for
the game deck. It handles rank and suit validation, determines numeric valuation for
Blackjack scoring, and supports serialization and deserialization. 
"""

__author__ = 'Adrien P.'

from typing import Any, Self

from constants import (
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
                f"'Clubs', 'Diamonds', 'Hearts', 'Spades'."
            )

        if isinstance(rank, int) and (2 <= rank <= 10):
            self.rank = rank
        elif isinstance(rank, str) and rank.capitalize() in NAMED_CARD_RANKS:
            self.rank = rank.capitalize()
        else:
            raise ValueError(
                f'Invalid rank, `rank` must be one of: '
                f"'2' through '10', 'Jack', 'King', 'Queen', 'Ace'."
            )
    
    def __eq__(self, other: object) -> bool:
        """Return `True` if this `Card` equals the other `Card`."""
        if not isinstance(other, Card):
            return False

        return (self.suit, self.rank) == (other.suit, other.rank)
    
    def __repr__(self) -> str:
        """e.g., Card(suit='Diamonds', rank='5')."""
        return f"Card(suit='{self.suit}', rank='{self.rank}')"
    
    def __str__(self) -> str:
        """e.g., ♦5."""
        return f'{CARD_SUIT_SYMBOLS[self.suit]}{self.rank}'
    
    @property
    def rank_value(self) -> int:
        """The numeric value of the `Card`. Aces are `11`, face cards are `10`."""
        if isinstance(self.rank, int):
            return self.rank
        
        if self.rank == ACE:
            return DEFAULT_ACE_VALUE
        
        return FACE_CARD_VALUE

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `Card` instance from a dictionary.
        
        Args:
            data (dict[str, Any]): A dictionary containing `suit` and `rank`.
        
        Returns:
            Self: A new Card instance.

        Raises:
            KeyError: If `suit` or `rank` is missing.
        """
        return cls(suit=data['suit'], rank=data['rank'])
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize the `Card` into a dictionary with `suit` and `rank`."""
        return {'suit': self.suit, 'rank': self.rank}
