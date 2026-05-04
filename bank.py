"""
Manages the storage of a player's chips. 

This module provides the `Bank` class, which acts as a player's wallet and manages,
modifies, and stores casino chips based on the player's current game state, as well
as supports serialization/deserialization.
"""

__author__ = 'Adrien P'

from typing import Any, Self

from constants import MAX_BANK

class Bank:
    """
    Represents a player's wallet for storing casino chips.

    Attributes:
        chips (float): The current total count of chips that the player owns.
    """
    def __init__(self, chips: float) -> None:
        """
        Initialize the player's `Bank` with the given amount of chips.

        Args:
            chips (float): The amount of chips to add to the player's bank.

        Raises:
            ValueError: If the `chips` value is not a valid number, is less than 0,
                or exceeds the maximum allowed bounds.
        """
        chips = self._to_float(chips)

        if not (0 <= chips <= MAX_BANK):
            raise ValueError(
                f'Invalid value, `chips` must be a number between '
                f'0 and {MAX_BANK:,.2f}.'
            )

        self.chips = chips

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
    def chips(self) -> float:
        """
        float: The player's current chip balance.

        Raises:
            ValueError: If the assigned value is less than 0 or cannot be converted
                to a float.
        """
        return self._chips

    @chips.setter
    def chips(self, value: float) -> None:
        value = self._to_float(value)

        if value < 0:
            raise ValueError('Invalid value, `value` is less than 0.')

        self._chips = value

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Build a `Bank` from a dictionary"""
        return cls(chips=data['chips'])
    
    def to_dict(self) -> dict[str, float]:
        """Pack the `Bank` into a dictionary."""
        return {'chips': self.chips}
    
    def to_string(self) -> str:
        """
        Return the string representation of the player's `Bank`.

        Returns:
            str: The string representation (e.g., Chips: $15.00).
        """
        return f'Chips: ${self.chips:,.2f}'
