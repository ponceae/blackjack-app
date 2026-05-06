from typing import Any, Self

from card import Card
from dataclasses import dataclass, field

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
    cards: list[Card] = field(default_factory=list)    
    
    @property
    def value(self):
        pass
    
    @property
    def hard_value(self):
        pass
    
    @property
    def is_soft(self):
        pass
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `Hand` from a dictionary.

        Validates that `value` is an int and `cards` is a list, and constructs
        Card instances from the provided card data.
        
        Args:
            data (dict[str, Any]): A dictionary containing:
                - value (int, optional): The current value of the hand. Defaults 
                    to `0`.
                - cards (list[dict]): Data used to construct `Card` instances. 
                    Defaults to an empty list.
                
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
        """Serialize the `Hand` into a dictionary with `value` and `cards` fields."""
        return {'value': self.value, 'cards': [card.to_dict() for card in self.cards]}

@dataclass
class DealerHand(Hand):
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
        
        hidden = data.get('is_face_up', True)
        _validate_type('is_face_up', hidden, bool)
        
        instance.is_face_up = hidden
        
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
