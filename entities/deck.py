""" 
Manages and modifies the state of a Blackjack game deck.

This module creates a standard 52 card deck and has functionality for shuffling and
drawing a card from the deck, and provides serialization and deserialization for
state persistence.
"""

__author__ = 'Adrien P.'

import random
from typing import Any, Self

from . import Card
from constants import CARD_RANKS, CARD_SUITS
from dataclasses import dataclass, field
from utils import validation

def create_deck() -> list[Card]:
    """Create and return a list containing 52 `Card` objects."""
    return [Card(suit, rank) for suit in CARD_SUITS for rank in CARD_RANKS]

@dataclass
class Deck:
    """
    Represents a standard deck of playing cards used in Blackjack.

    Attributes:
        cards (list[Card]): The current deck of cards at the table.
    """
    cards: list[Card] = field(default_factory=create_deck)    
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `Deck` from a dictionary.

        Validates that `cards` is a list, and constructs Card instances from the 
        provided card data.

        Args:
            data (dict[str, Any]): A dictionary containing:
                - cards (list[dict], optional): Data used to construct `Card`
                    instances. Defaults to a standard 52 card deck.

        Returns:
            Self: A new Deck instance.

        Raises:
            KeyError: If `cards` is missing from the data.
            TypeError: If `cards` is not a list.
        """
        indices = data['cards']
        validation.validate_type('cards', indices, list)

        master_deck = create_deck()
        
        rebuilt_cards = [master_deck[i] for i in indices]

        return cls(cards=rebuilt_cards)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the current `Deck` state into a dictionary.
        
        Returns:
            dict[str, Any]: A dictionary containing serialized `Card` instances.
        """
        master_deck = create_deck()
        
        indices = [master_deck.index(card) for card in self.cards]
        
        return {'cards': indices}

    def shuffle(self) -> None:
        """
        Shuffle the given list of `Card` objects.
        """
        random.shuffle(self.cards)
    
    def draw_card(self) -> Card:
        """Draw and return a `Card` from the deck, resetting the deck if empty."""
        if not self.cards:
            self.reset()

        return self.cards.pop()

    def reset(self) -> None:
        """Create and shuffle a new 52 card deck."""
        self.cards = create_deck()
        self.shuffle()
