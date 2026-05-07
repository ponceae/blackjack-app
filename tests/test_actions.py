""" 
Tests for the `actions.py` module.

Validates hand values, ensures that hitting and splitting adds the correct
amount of cards to the hand, and that only two cards are dealt at the beginning
of the round.
"""

__author__ = 'Adrien P.'

import pytest

import actions
from entities.card import Card
from datatypes import Player, Table
from entities.hand import Hand, PlayerHand

# @pytest.fixture
# def table() -> Table:
#     """Provide a `Table` instance preloaded with only a deck."""
#     return Table(player=Player(username='Test'), deck=actions.create_and_shuffle())

# def test_create_split_hands_created_new_hand(table):
#     table.player.hands = [PlayerHand(cards=[Card('Clubs', 6), Card('Hearts', 6)])]

#     actions.create_split_hands(table)

#     assert len(table.player.hands) == 2

#     assert str(table.player.hands[0].cards[0]) == '♣6'
#     assert str(table.player.hands[1].cards[0]) == '♥6'

# def test_hit_hand_added_card_to_hand(table):
#     table.player.hands = [PlayerHand(cards=[Card('Clubs', 4), Card('Hearts', 6)])]
#     actions.hit_hand(table, table.player.hands[0])

#     assert len(table.player.hands[0].cards) == 3

# def test_hit_hand_continues_after_empty_deck(table):
#     table.player.hands = [PlayerHand(cards=[])]    
#     table.deck.clear()

#     actions.hit_hand(table, table.player.hands[0])

#     assert len(table.player.hands[0].cards) == 1

# def test_initial_round_dealt_correct_num_cards_to_hands(table):
#     actions.initial_round_deal(table)

#     assert len(table.player.hands) == 1
#     assert len(table.player.hands[0].cards) == 2

#     assert len(table.dealer.cards) == 2

# def test_initial_round_deal_success_on_empty_deck(table):
#     table.deck.clear()
#     actions.initial_round_deal(table)

#     assert len(table.player.hands) == 1
#     assert len(table.player.hands[0].cards) == 2

#     assert len(table.dealer.cards) == 2
