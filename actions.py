"""
Blackjack game actions and calculations.

This module contains functions to deal cards, manage hands, and 
calculate hand values and payouts.
"""

__author__ = 'Adrien P.'

from entities.card import Card
from constants import ACE_ALT_VALUE, DEFAULT_ACE_VALUE
from entities.hand import DealerHand, Hand, PlayerHand
from datatypes import Table
from deck import create_deck, shuffle_deck

def create_split_hands(table: Table) -> None:
    """
    Create a new `PlayerHand` by popping a card from the first initial hand and
    hitting both hands.

    Args:
        table (Table): The table containing the player's hand and the deck of cards.
    """
    table.player.hands.append(PlayerHand(cards=[table.player.hands[0].cards.pop()]))

    for hand in table.player.hands:
        hit_hand(table, hand)

def hit_hand(table: Table, hand: Hand) -> None:
    """
    Draw a card from the table's deck and add it to the hand. Create and shuffle a 
    new deck if the game deck is empty.

    Args:
        table (Table): The table containing the current hand and the deck of cards.
        hand (Hand): The current hand being modified.
    """
    if not table.deck:
        table.deck = create_and_shuffle()

    hand.cards.append(table.deck.pop())

def initial_round_deal(table: Table) -> None:
    """
    Initialize a `PlayerHand` and a `DealerHand` on the table by dealing both 
    two cards each.

    Args:
        table (Table): The table containing the `PlayerHand`, the `DealerHand`, and  
            the deck of cards.
    """
    table.player.hands = [PlayerHand()]
    table.dealer = DealerHand()

    for i in range(4):
        if not table.deck:
            table.deck = create_and_shuffle()	

        card = table.deck.pop()

        if i % 2 == 0:
            table.player.hands[0].cards.append(card)
        else:
            table.dealer.cards.append(card)

def get_hard_value(hand: Hand) -> int:
    """
    Return the total numeric value of the hand, counting all Aces as a 1.

    Args:
        hand (Hand): The hand to calculate.

    Returns:
        int: The final calculated hand value.
    """
    value = 0

    for card in hand.cards:
        if card.rank == 'Ace':		
            value += ACE_ALT_VALUE 
        else:
            value += card.rank_value

    return value

def create_and_shuffle() -> list[Card]:
    """Create, shuffle, and return a new 52-card deck."""
    return shuffle_deck(create_deck())
