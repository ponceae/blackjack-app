""" 
Manages the logic and state of a Blackjack hand.

This module provides a `Hand` dataclass for storing cards, value, and state, along
with `PlayerHand` `DealerHand` subclasses for specialized game roles. It supports
automatic value calculation and provides methods for serialization and deserialization.
"""

__author__ = 'Adrien P.'

from typing import Any, Self

from card import Card
from constants import ACE_ALT_VALUE, DEFAULT_ACE_VALUE
from dataclasses import dataclass, field

# ==========================
# Private Helper Functions.
# ==========================

def _validate_type(field_name: str, value: Any, expected_type: type | tuple) -> None:
    """Enforce strict type checking during deserialization."""
    if not isinstance(value, expected_type):
        if isinstance(expected_type, tuple):
            type_names = ' or '.join(t.__name__ for t in expected_type)
        else:
            type_names = expected_type.__name__
            
        raise TypeError(
            f'Expected `{field_name}` to be `{type_names}`, '
            f'got {type(value).__name__}'
        )

@dataclass
class Hand:
    """ 
    A base collection of cards with Blackjack scoring logic.
    
    This class serves as the parent for all hand types, providing automatic
    calculation of soft and hard hand values and manages the card collection.
    
    Attributes:
        cards (list[Card], optional): The cards currently in the hand. Defaults to an 
            empty list. 
    """
    cards: list[Card] = field(default_factory=list)    
    
    @property
    def value(self) -> int:
        """
        Return the optimal numeric vale of the hand.

        Count the score by initially valuing Aces at 11, then contextually 
        downgrading Ace values to 1 when needed to avoid exceeding 21.

        Returns:
            int: The highest possible score that is 21 or less.
        """
        value, ace_count = 0, 0

        for card in self.cards:
            if card.rank == 'Ace':	
                value += DEFAULT_ACE_VALUE 
                ace_count += 1 
            else:
                value += card.rank_value

        while ace_count > 0 and value > 21: 
            value -= DEFAULT_ACE_VALUE
            value += ACE_ALT_VALUE 
            ace_count -= 1

        return value
    
    @property
    def hard_value(self) -> int:
        """
        Return the total numeric value of the hand, counting all Aces as a 1.

        Returns:
            int: The final calculated hand value.
        """
        value = 0

        for card in self.cards:
            if card.rank == 'Ace':		
                value += ACE_ALT_VALUE 
            else:
                value += card.rank_value

        return value
    
    @property
    def is_soft(self) -> bool:
        """
        Return `True` if the hand contains an Ace currently valued at 11.

        Returns:
            bool: `True` if the hand is soft, `False` otherwise.
        """
        return self.hard_value != self.value
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `Hand` from a dictionary.

        Validates that `value` is an int and `cards` is a list, and constructs
        Card instances from the provided card data.
        
        Args:
            data (dict[str, Any]): A dictionary containing:
                - cards (list[dict], optional): Data used to construct `Card` 
                    instances. Defaults to an empty list.
                
        Returns:
            Self: A new Hand instance.
            
        Raises:
            TypeError: If `value` is not an int or `cards` is not a list.
        """
        instance = cls()
        
        raw_cards = data.get('cards', [])
        _validate_type('cards', raw_cards, list)
        
        instance.cards = [Card.from_dict(card) for card in raw_cards]
        
        return instance
            
    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the current `Hand` state into a dictionary.
        
        Returns:
            dict[str, Any]: A dictionary containing:
            - cards (list[dict]): Serialized Card instances
            - value (int): The optimal Blackjack hand score.
            - hard_value (int): The hand score with all Aces counted as 1.
            - is_soft (bool): True if the hand contains a soft Ace.
        """
        return {
            'cards': [card.to_dict() for card in self.cards],
            'value': self.value,
            'hard_value': self.hard_value,
            'is_soft': self.is_soft,
        }

@dataclass
class DealerHand(Hand):
    """ 
    A specialized hand belonging to the dealer, including its hole card state.
    
    Attributes:
        is_face_up (bool): The state of the dealer's hole card, whether it is face up
            or not. Defaults to `False`
    """
    is_face_up: bool = False
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `DealerHand` from a dictionary.
        
        Delegates parsing and validation of `value` and `cards` to `Hand.from_dict`.
        Validates that the `is_face_up` field is a bool. 

        Args:
            data (dict[str, Any]): A dictionary containing base `Hand` fields and:
                - is_face_up (bool): Whether the dealer's first card is face up.
                    Defaults to `False`.
        
        Returns:
            Self: A new DealerHand instance.
        
        Raises:
            TypeError: If `is_face_up` is not a bool.
        """
        instance = super().from_dict(data)
        
        face_up = data.get('is_face_up', False)
        _validate_type('is_face_up', face_up, bool)
        
        instance.is_face_up = face_up
        
        return instance

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the `DealerHand` into a dictionary, extending base `Hand` fields with 
        the `is_face_up` state.
        """
        data = super().to_dict()
        
        data['is_face_up'] = self.is_face_up
        
        return data

@dataclass
class PlayerHand(Hand):
    """ 
    A specialized hand belonging to a player, including the betting state and hand
    current hand status.
    
    Attributes:
        wager (float, optional): The hand's current wager. Defaults to `0.0`.
        insurance_wager (float, optional): The hand's current insurance_wager. 
            Defaults to `0.0`.
        is_current (bool, optional): Whether this specific hand is currently being 
            played with respect to split hands. Defaults to `False`.
    """
    wager: float = 0.0
    insurance_wager: float = 0.0
    is_current: bool = False
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """ 
        Create a `PlayerHand` from a dictionary.
        
        Delegates parsing and validation of `value` and `cards` to `Hand.from_dict`.
        Validates that the `wager` and `insurance_wager` fields are numeric,  and 
        that the `is_current` state is a bool.
        
        Args:
            data (dict[str, Any]): A dictionary containing base `Hand` fields and:
                - wager (float): The current wager on the hand.
                - insurance_wager (float): The current insurance wager on the hand.
                - is_current (bool): Whether this specific hand is currently being
                    played (relevant during split hands).
        
        Returns:
            Self: A new PlayerHand instance.
            
        Raises:
            TypeError: If `wager` or `insurance_wager` is not a number, or if 
                `is_current` is not a bool.
        """
        instance = super().from_dict(data)

        raw_wager = data.get('wager', 0.0)
        _validate_type('wager', raw_wager, (int, float))
          
        raw_insurance_wager = data.get('insurance_wager', 0.0)
        _validate_type('insurance_wager', raw_insurance_wager, (int, float))
                    
        current = data.get('is_current', False)
        _validate_type('is_current', current, bool)

        instance.wager = float(raw_wager)
        instance.insurance_wager = float(raw_insurance_wager)
        instance.is_current = current    
        
        return instance

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        
        data['wager'] = self.wager
        data['insurance_wager'] = self.insurance_wager
        data['is_current'] = self.is_current
        
        return data
