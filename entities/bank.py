"""
Manages the storage of a player's chips. 

This module provides the `Bank` class, which acts as a player's wallet and manages,
modifies, and stores casino chips based on the player's current game state, and 
supports serialization/deserialization.
"""

__author__ = 'Adrien P'

from typing import Any, Self

from constants import MAX_STARTING_CAP

class Bank:
    """
    Represents a player's wallet for storing their money.

    Attributes:
        balance (float): The current total balance of the player.
    """
    def __init__(self, balance: float) -> None:
        """
        Initialize the player's `Bank` with the given amount of chips.

        Args:
            chips (float): The amount of chips to add to the player's bank.

        Raises:
            ValueError: If the `chips` value is not a valid number, is less than 0,
                or exceeds the maximum allowed bounds.
        """
        balance = self._to_float(balance)

        if not (0 <= balance <= MAX_STARTING_CAP):
            raise ValueError(
                f'Invalid value, `balance` must be a number between '
                f'0 and {MAX_STARTING_CAP:,.2f}.'
            )

        self.balance = balance

    def __eq__(self, other: object) -> bool:
        """Return `True` if this `Bank` equals the other `Bank`."""
        if not isinstance(other, Bank):
            return False
        
        return self.balance == other.balance
    
    def __repr__(self) -> str:
        """e.g., Bank(balance='34.5')."""
        return f"Bank(balance='{self.balance}')"
    
    def __str__(self) -> str:
        """e.g., Balance: $34.50."""
        return f'Balance: ${self.balance:,.2f}'

    @staticmethod
    def _to_float(value: Any) -> float:
        """ 
        Validate value type and handle float conversion.

        Args:
            value (Any): The value to validate and convert.

        Returns:
            float: The converted value.

        Raises:
            ValueError: If the value cannot be converted to a float.
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError('Invalid value, `value` must be a number.')

    @property
    def balance(self) -> float:
        """
        float: The player's current balance.

        Raises:
            ValueError: If the assigned value is less than 0 or cannot be converted
                to a float.
        """
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        value = self._to_float(value)

        if value < 0:
            raise ValueError('Invalid value, `value` is less than 0.')

        self._balance = value

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `Bank` from a dictionary.
        
        Args:
            data (dict[str, Any]): A dictionary containing `balance`.

        Returns:
            Self: A new Bank instance.

        Raises:
            KeyError: If `balance` is missing.
        """
        return cls(balance=data['balance'])
    
    def to_dict(self) -> dict[str, float]:
        """Serialize the `Bank` into a dictionary with `balance`."""
        return {'balance': self.balance}
