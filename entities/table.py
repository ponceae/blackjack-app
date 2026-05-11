from dataclasses import dataclass, field
from typing import Any, Self

from . import DealerHand, Deck, Player
from utils import validation

@dataclass
class Table:
    """
    Represents the Blackjack game table.

    Attributes:
        player (Player): The sitting player.
        dealer (Dealer): The standing dealer.
        deck (Deck): The current game deck.
    """
    player: Player
    dealer: DealerHand = field(default_factory=DealerHand)
    deck: Deck = field(default_factory=Deck)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a `Table` instance from a dictionary.

        Validates that `player` is a Player, `dealer` is a DealerHand, `deck` is a 
        Deck, and constructs a `Table` instance from the provided data.

        Args:
            data (dict[str, Any]): A dictionary containing:
                - player (Player): The sitting player.
                - dealer (Dealer): The standing dealer.
                - deck (Deck): The current game deck.
        
        Returns:
            Self: A new Table instance.

        Raises:
            KeyError: If `player`, `dealer`, or `deck` is missing from the data.
            TypeError: If `player` is not a Player, `dealer` is not a DealerHand,
                and `deck` is not a Deck.
        """
        validation.validate_type('player', Player.from_dict(data['player']), Player)

        validation.validate_type(
            'dealer', DealerHand.from_dict(data['dealer']), DealerHand
        )

        validation.validate_type('deck', Deck.from_dict(data['deck']), Deck)

        return cls(
            player=Player.from_dict(data['player']),
            dealer=DealerHand.from_dict(data['dealer']),
            deck=Deck.from_dict(data['deck']),
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the current `Table` state into a dictionary.
        
        Returns:
            dict[str, Any]: A dictionary containing a serialized `Table` instance.
        """
        return {
            'player': self.player.to_dict(),
            'dealer': self.dealer.to_dict(),
            'deck': self.deck.to_dict(),
        }
