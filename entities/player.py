""" 
Manages the state of a player at a Blackjack table.

This module provides a Player class with the following functionality:
    - Add a hand to the player or reset the player's hands.
    - Add or remove a monetary amount from the player's hands.
    - Count the number of player hands.
    - Check the status of a the player's hands.
    - Validate if the current player can afford a wager.
    - Provide serialization and deserialization for state persistence.
"""

__author__ = 'Adrien P.'

from typing import Any, Self

from . import PlayerHand, Bank
from dataclasses import dataclass, field
from utils import validation

@dataclass
class Player:
    """
    Represents a player at the table, including their bank balance and hands.

    Attributes:
        bank (Bank): The current player's bank containing their overall balance.
        hands (list[PlayerHand]): The current player's game hands at the table.
    """
    bank: Bank = field(default_factory=lambda: Bank(500))
    hands: list[PlayerHand] = field(default_factory=list)

    @classmethod 
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `Player` from a dictionary.
        
        Validates that `bank` is a Bank and `hands` is a list, and constructs a
        `Player` instance from the provided data.

        Args:
            data (dict[str, Any]): A dictionary containing:
                - bank (Bank): The player's finances.
                - hands (list[PlayerHand]): The player's game hands.

        Returns: 
            Self: A new Player instance.

        Raises:
            KeyError: If `bank` or `hands` is missing from the data.
            TypeError: if `bank` is not a Bank or `hands` is not a list.
        """
        validation.validate_type('bank', Bank.from_dict(data['bank']), Bank)

        raw_hands = data['hands']
        validation.validate_type('hands', raw_hands, list)

        return cls(
            bank=Bank.from_dict(data['bank']), 
            hands=[PlayerHand.from_dict(hand_data) for hand_data in raw_hands]
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the current `Player` state into a dictionary.
        
        Returns:
            dict[str, Any]: A dictionary containing a serialized `Player` instance.
        """
        return {
            'bank': self.bank.to_dict(), 
            'hands': [_hands.to_dict() for _hands in self.hands]
        }

    def add_hand(self, hand: PlayerHand) -> None:
        """Add the provided hand to the current player's hands."""
        self.hands.append(hand)

    def reset(self) -> None:
        """Clear the player's hands."""
        self.hands.clear()

    def add_balance(self, amount: float) -> None:
        """Add the amount to the player's balance."""
        self.bank.balance += amount

    def remove_balance(self, amount: float) -> None:
        """Remove the amount from the player's balance."""
        self.bank.balance -= amount

    def can_afford(self, amount: float) -> bool:
        """Return `True` if the current player can afford the provided amount."""
        return self.bank.balance >= amount
    
    def count(self) -> int:
        """Return the current count of the player's hands."""
        return len(self.hands)
    
    def has_active_hands(self) -> bool:
        """Return `True` if the current player contains at least one hand."""
        return self.count() > 0
