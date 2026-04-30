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
from typing import NamedTuple

from .bank import Bank
from .card import Card

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

@dataclass
class DealerHand(Hand):
    is_hidden: bool = True

@dataclass
class PlayerHand(Hand):
    wager: float = 0.0
    insurance_wager: float = 0.0
    is_active: bool = False

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
