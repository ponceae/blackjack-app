""" 
Data containers for game state information.

Provides the core data structures used to track game state, including:
- Dataclasses for entities (Player, Dealer, Hands, and the Table)
- Dataclasses for round mechanics (Insurance, Outcomes, and Splits)
- Enums and NamedTuples for tracking actions and UI buffers
"""

__author__ = 'Adrien P.'

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, NamedTuple, Self

from bank import Bank
from card import Card

# ==============================
# BLACKJACK ACTIONS AND DISPLAY
# ==============================

class Buffers(NamedTuple):
    """Stores output display for game state changes."""
    dealer: list
    player: list
    main: list

class PlayerAction(Enum):
    NEXT_HAND = 1
    END_TURN = 2

# ==========================
# BLACKJACK ROUND MECHANICS
# ==========================

@dataclass
class Insurance():
    active: bool = False
    win: bool = False
    payout: float = 0
    cost: float = 0

@dataclass
class Outcome():
    """Tracks winning entity flag and the corresponding payout."""
    flag: int = 0
    payout: float = 0

@dataclass
class SplitHands:
    split_hand: bool = False
    split_aces: bool = False

# ===================
# BLACKJACK ENTITIES
# ===================

@dataclass
class Hand:
    value: int = 0
    cards: list[Card] = field(default_factory=list)    
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `Hand` from a dictionary.

        Validates that `value` is an int and `cards` is a list, and constructs
        Card instances from the provided card data.
        
        Args:
            data (dict[str, Any]): A dictionary containing:
                - value (int): The current value of the hand. Defaults to `0` if not
                    provided.
                - cards (list[dict]): Data used to construct `Card` instances.
                
        Returns:
            Hand: A new Hand instance.
            
        Raises:
            TypeError: If `value` is not an int or `cards` is not a list.
        """
        raw_value = data.get('value', 0) 
        if not isinstance(raw_value, int):
            raise TypeError(f'Hand `value` must be int, got {type(raw_value)}')
        
        raw_cards = data.get('cards', [])
        if not isinstance(raw_cards, list):
            raise TypeError(f'Hand `cards` must be list, got {type(raw_cards)}')
        
        card_data = [Card.from_dict(card) for card in raw_cards]
        
        return cls(value=raw_value, cards=card_data)
    
    def to_dict(self) -> dict[str, int | list[dict[str, Any]]]:
        """Serialize the `Hand` into a dictionary with `value` and `cards`."""
        return {'value': self.value, 'cards': [card.to_dict() for card in self.cards]}

@dataclass
class DealerHand(Hand):
    is_hidden: bool = True
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `DealerHand` from a dictionary.
        
        Delegates parsing and validation of `value` and `cards` to `Hand.from_dict`.
        Validates that the `is_hidden` field is a bool. 

        Args:
            data (dict[str, Any]): A dictionary containing:
                - value (int): See Hand.from_dict.
                - cards (list[dict]): See Hand.from_dict.
                - is_hidden (bool): Whether the dealer's hand is hidden. Defaults to
                    `True` if not provided.

        Returns:
            DealerHand: A new DealerHand instance.
        
        Raises:
            TypeError: if `is_hidden` is not a bool.
        """
        hand = Hand.from_dict(data)
        
        hidden = data.get('is_hidden', True)
        
        if not isinstance(hidden, bool):
            raise TypeError(f'DealerHand `is_hidden` must be bool, got {type(hidden)}')
        
        return cls(value=hand.value, cards=hand.cards, is_hidden=hidden)
    
    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the `DealerHand` into a dictionary, including the `is_hidden` field.
        """
        data = super().to_dict()
        
        data['is_hidden'] = self.is_hidden
        
        return data

@dataclass
class PlayerHand(Hand):
    wager: float = 0.0
    insurance_wager: float = 0.0
    is_active: bool = False
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        hand = Hand.from_dict(data)

        raw_wager = data.get('wager', 0.0)
        if not isinstance(raw_wager, float):
            raise TypeError(f'PlayerHand `wager` must be float, got {type(raw_wager)}')
        
        raw_insurance_wager = data.get('insurance_wager', 0.0)
        if not isinstance(raw_insurance_wager, float):
            raise TypeError(
                f'PlayerHand `insurance_wager` must be float, '
                f'got {type(raw_insurance_wager)}'
            )
        
        active = data.get('is_active', False)
        if not isinstance(active, bool):
            raise TypeError(f'PlayerHand `is_active` must be bool, got {type(active)}')
        
        return cls(
            value=hand.value, 
            cards=hand.cards, 
            wager=raw_wager, 
            insurance_wager=raw_insurance_wager, 
            is_active=active
        )

    def to_dict(self) -> dict[str, Any]:
        pass

@dataclass
class Player:
    username: str
    bank: Bank = field(default_factory=lambda: Bank(0))
    hands: list[PlayerHand] = field(default_factory=list)

@dataclass
class Table:
    player: Player
    dealer: DealerHand = field(default_factory=DealerHand)
    deck: list[Card] = field(default_factory=list)
