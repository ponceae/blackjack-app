""" 
Tests for the `actions.py` module.

Validates the game table initialization and:
    - Ensures hitting a hand removes a card from the deck and adds it to the correct 
        hand.
    - Ensures that splitting a hand initializes a new `PlayerHand` object and adds it 
        to the player.
"""

__author__ = 'Adrien P.'

import pytest

from entities import Card, Player, PlayerHand, Table
from engine import actions

@pytest.fixture
def table() -> Table:
    """Provide a default table with a bank balance of 500.0 and an empty hand."""
    table = Table(player=Player())
    return table

def test_deal_initial_initializes_game_table(table):
    test_table = actions.deal_initial_cards(table)

    assert test_table.player.count() == 1
    assert len(test_table.player.hands[0].cards) == 2

    assert len(test_table.dealer.cards) == 2

    assert len(test_table.deck.cards) == 48

def test_hit_hand_adds_card_to_deck_and_returns_expected_card(table):  
    table.player.add_hand(PlayerHand())
      
    card_a = actions.hit_hand(table, table.player.hands[0])
    card_b = actions.hit_hand(table, table.dealer)
    
    assert len(table.deck.cards) == 50
    
    assert table.player.count() == 1
    assert len(table.dealer.cards) == 1
    
    assert card_a == Card('Spades', 'Ace')
    assert card_b == Card('Spades', 'King')
    
def test_split_hand_creates_new_playerhand(table):
    test_table = actions.deal_initial_cards(table)
        
    test_table = actions.split_hand(test_table)
    
    assert len(test_table.deck.cards) == 46
    
    assert table.player.count() == 2

def test_dealer_turn(table):    
    table.dealer.add_card(Card('Spades', 10))
    table.dealer.add_card(Card('Clubs', 6))
    
    table = actions.dealer_turn(table)
    
    assert len(table.dealer.cards) == 3
    assert table.dealer.is_face_up == True

def test_handle_stand_hands_left(table):
    table.player.add_hand(PlayerHand())
    table.player.add_hand(PlayerHand())
    
    cond = actions.handle_stand(table)
    
    assert cond == True
    
def test_handle_stand_no_hands_left(table):
    table.player.add_hand(PlayerHand())
    
    cond = actions.handle_stand(table)
    
    assert cond == False
    