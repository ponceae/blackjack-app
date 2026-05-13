""" 
Test data generators and mappings for `test_table.py`.

Provides:
    - Table object generator.
    - Dictionary factory for Table. 
"""

__author__ = 'Adrien P.'

from typing import Any

from entities import Bank, Card, Deck, DealerHand, Player, PlayerHand, Table

def _generate_deck_with_drawn_cards(amount) -> Deck:
    """Generate a deck with the specified amount of card objects missing."""
    deck = Deck()
    
    for _ in range(amount):
        deck.cards.pop()
    
    return deck

def _generate_table_objects() -> list[Table]:
    """Provide a list of `Table` objects."""
    return [
        Table(
            player=Player(
                bank=Bank(250.0), 
                hands=[
                    PlayerHand(
                        cards=[
                            Card('Spades', 5), 
                            Card('Hearts', 7),
                            Card('Diamonds', 10),
                        ], 
                        wager=15.0, 
                        insurance_wager=7.5, 
                        is_current=True,
                    ), 
                    PlayerHand(
                        cards=[Card('Diamonds', 'Ace'), Card('Clubs', 4)],
                        wager=15.0,
                    ),
                ],
            ),
            dealer=DealerHand(cards=[Card('Diamonds', 5), Card('Hearts', 10)]),
            deck=_generate_deck_with_drawn_cards(6),
        ),
        Table(
            player=Player(
                bank=Bank(500.0), 
                hands=[
                    PlayerHand(
                        cards=[Card('Diamonds', 9), Card('Spades', 10)], 
                        wager=50.0, 
                        is_current=True,
                    ), 
                ],
            ),
            dealer=DealerHand(
                cards=[Card('Clubs', 10), Card('Hearts', 9)],
                is_face_up=True
            ),
            deck=_generate_deck_with_drawn_cards(4)
        ),
        Table(
            player=Player(
                bank=Bank(750.0), 
                hands=[
                    PlayerHand(
                        cards=[Card('Hearts', 'Queen'), Card('Spades', 'Ace')], 
                        wager=27.5, 
                    ), 
                    PlayerHand(
                        cards=[Card('Clubs', 'Jack'), Card('Hearts', 10)], 
                        wager=27.5, 
                        is_current=True,
                    ),
                ],
            ),
            dealer=DealerHand(cards=[Card('Clubs', 4), Card('Diamonds', 9)]),
            deck=_generate_deck_with_drawn_cards(6)
        ),
        Table(
            player=Player(
                bank=Bank(146.7), 
                hands=[
                    PlayerHand(
                        cards=[
                            Card('Hearts', 4), 
                            Card('Spades', 'King'), 
                            Card('Diamonds', 10),
                        ], 
                        wager=65.75, 
                        is_current=True
                    ), 
                    PlayerHand(
                        cards=[Card('Clubs', 7), Card('Hearts', 10)], 
                        wager=27.5,
                        insurance_wager=13.5
                    ),
                ],
            ),
            dealer=DealerHand(
                cards=[Card('Clubs', 4), Card('Diamonds', 'King'), Card('Spades', 4)],
                is_face_up=True
            ),
            deck=_generate_deck_with_drawn_cards(6)
        ),
    ]

def table_mapping_pairs() -> list[tuple[Table, dict[str, Any]]]:
    """Generate pairs of `Table` {'player', 'dealer', 'deck'} dicts."""
    return [
        (
            table, 
            {
                'player': table.player.to_dict(), 
                'dealer': table.dealer.to_dict(), 
                'deck': table.deck.to_dict()
            }
        )
        for table in _generate_table_objects()
    ]
