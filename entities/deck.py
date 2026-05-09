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
    cards: list[Card] = field(default_factory=create_deck)    
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `Deck` from a dictionary.
        """
        pass

    def to_dict(self):
        pass

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
