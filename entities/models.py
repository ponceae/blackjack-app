""" 
Schemas for managing game states.

Acts as the state manager for:
    - Insurance status, payout, and cost.
    - Blackjack round outcomes and payouts.
"""

__author__ = 'Adrien P.'

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Self

from utils import validation

@dataclass
class Insurance:
    """ 
    The state manager for round insurance status.
    
    Attributes:
        active (bool): Whether insurance has been purchased and if the condition is yet
            to be checked.
        win (bool): If insurance has been won on the current round.
        payout (float): The insurance payout to the player.
        cost (float): The cost for purchasing insurance.
    """
    active: bool = False
    win: bool = False
    payout: float = 0.0
    cost: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """ 
        Create an `Insurance` instance from a dictionary.
        
        Validates that `active` and `win` are each a bool, and that the `payout` and 
        `cost` fields are numeric .
        
        Args:
            data (dict[str, Any]): A dictionary containing:
                - active (bool): Whether insurance is purchased.
                - win (bool): If insurance was won.
                - payout (float): The insurance payout to the player.
                - cost (float): The cost for purchasing insurance.
            
        Returns:
            Self: A new Insurance instance.
            
        Raises:
            KeyError: If `active`, `win`, `payout`, or `cost` are missing from 
                the data.
            TypeError: If `active` or `win` are not a bool, or if `payout` or `cost`
                are not numbers.
        """
        _active = data['active']
        validation.validate_type('active', _active, bool)
        
        _win = data['win']
        validation.validate_type('win', _win, bool)
        
        raw_payout = data['payout']
        validation.validate_type('payout', raw_payout, (int, float))
        
        raw_cost = data['cost']
        validation.validate_type('cost', raw_cost, (int, float))
    
        return cls(active=_active, win=_win, payout=raw_payout, cost=raw_cost)
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize the current `Insurance` state into a dictionary."""
        return {
            'active': self.active,
            'win': self.win,
            'payout': self.payout,
            'cost': self.cost,
        }
    
    def reset(self) -> None:
        """Revert `Insurance` to its default, empty state."""
        self.active = False
        self.win = False
        self.payout = 0.0
        self.cost = 0.0
    
class OutcomeFlag(IntEnum):
    """ 
    Blackjack round states.
    
    Used to determine win/loss logic.
    """
    NONE = 0
    PLAYER_WIN = 1
    PLAYER_BLACKJACK = 2
    DEALER_WIN = 3
    DEALER_BLACKJACK = 4
    PUSH= 5

@dataclass
class Outcome:
    """
    The state manager for Blackjack round outcomes and payouts.
    
    Attributes:
        flag (OutcomeFlag): The current outcome of the Blackjack round.
        payout (float): The monetary amount to payout to the player.
    """
    flag: OutcomeFlag = OutcomeFlag.NONE
    payout: float = 0.0
    
    @classmethod
    def from_dict(cls, data) -> Self:
        """ 
        Create an `Outcome` instance from a dictioanry.
        
        Validates that `flag` is an int and in `OutcomeFlag`, and that `payout` is a 
        number.
        
        Args:
            data (dict[str, Any]): A dictionary containing:
                - flag (OutcomeFlag): The current Blackjack round outcome.
                - payout (float): The monetary amount to payout to the player.
                
        Raises:
            KeyError: If `flag` or `payout` is missing from data.
            TypeError: If `flag` is not an int or `payout` is not a number.
            ValueError: If `flag` is not in `OutcomeFlag`.
        """
        _flag = data['flag']
        validation.validate_type('flag', _flag, int)
        
        if _flag not in OutcomeFlag:
            raise ValueError(f'Invalid outcome code: {_flag}')
                
        raw_payout = data['payout']
        validation.validate_type('payout', raw_payout, (int, float))
        
        return cls(flag=OutcomeFlag(_flag), payout=raw_payout)
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize the current `Outcome` state into a dictionary."""
        return {
            'flag': int(self.flag),
            'payout': self.payout
        }
    
    def reset(self) -> None:
        """Revert `Outcome` to its default, empty state."""
        self.flag = OutcomeFlag.NONE
        self.payout = 0.0
