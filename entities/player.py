from dataclasses import dataclass, field

from . import PlayerHand, Bank

@dataclass
class Player:
    bank: Bank = field(default_factory=lambda: Bank(0))
    hands: list[PlayerHand] = field(default_factory=list)

    @classmethod