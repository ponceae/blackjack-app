""" 
Tests for the `actions.py` module.
"""

__author__ = 'Adrien P.'

import pytest

from entities import Player, Table
from engine import actions

@pytest.fixture
def table() -> Table:
    """Provide a default table with a bank balance of 500.0 and an empty hand."""
    return Table(player=Player())

def test_deal_initial_initializes_game_table(table):
    test_table = actions.deal_initial_cards(table)

    assert test_table.player.count() == 1
    assert len(test_table.player.hands[0].cards) == 2

    assert len(test_table.dealer.cards) == 2

    assert len(test_table.deck.cards) == 48

def test_hit_hand_adds_card_to_deck_and_returns_card():
    pass
