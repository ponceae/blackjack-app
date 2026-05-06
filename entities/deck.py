import random

from . import Card
from dataclasses import dataclass, field
from constants import CARD_RANKS, CARD_SUITS

def create_deck() -> list[Card]:
    """Create and return a list containing 52 `Card` objects."""
    return [Card(suit, rank) for suit in CARD_SUITS for rank in CARD_RANKS]

@dataclass
class Deck:
    cards: list[Card] = field(default_factory=create_deck)    
    
    @staticmethod 
    def shuffle_deck(deck: list[Card]) -> list[Card]:
        """
        Shuffle and return the given list of `Card` objects.
        
        Args:
            deck (list[Card]): The provided list to shuffle
        
        Returns:
            list[Card]: The shuffled list of Card objects.
        """
        for i in range(len(deck) - 1, 0, -1):
            j = random.randint(0, i)
            
            deck[i], deck[j] = deck[j], deck[i]

        return deck
