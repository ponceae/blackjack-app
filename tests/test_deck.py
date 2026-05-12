"""
Tests for the `deck.py` module.

Validates game deck initialization and modification, and ensures serialization
and deserialization creates valid data.
"""

__author__ = 'Adrien P.'

import pytest
from typing import Any

from entities import  Deck

@pytest.fixture
def deck() -> Deck:
    """Provide a `Deck` instance with an unshuffled deck."""
    return Deck()

@pytest.fixture
def deck_map_pair(deck) -> tuple[Deck, dict[str, Any]]:
    """Provide a pair of a `Deck` instance and a {`cards`} dict."""
    return (deck, {'cards': [c.to_dict() for c in deck.cards]})

# =========================================
# Deck Serialization/Deserialization Tests.
# =========================================

def test_from_dict_creates_deck_instances(deck_map_pair):
    test_deck = Deck.from_dict(deck_map_pair[1])

    assert test_deck.cards == deck_map_pair[0].cards

def test_to_dict_creates_correct_data_dict(deck_map_pair):
    data_dict = deck_map_pair[0].to_dict()

    assert data_dict == deck_map_pair[1]

# ========================================
# Deck Initialization and Shuffling Tests.
# ========================================

def test_create_deck_has_52_cards(deck):   
    assert len(deck.cards) == 52

def test_shuffle_deck_is_same_deck(deck):
    deck.shuffle()

    assert len(deck.cards) == 52

# =======================================
# Deck Instance Methods.
# ---------------------------------------
# Tests deck.reset() and deck.draw_card()
# =======================================

def test_reset_is_new_deck(deck):
    deck.draw_card()
    deck.reset()

    assert len(deck.cards) == 52

def test_draw_card_removes_one(deck):
    deck.draw_card()
    assert len(deck.cards) == 51
    
def test_draw_card_on_empty_deck(deck):
    deck.cards.clear()
    deck.draw_card()
    
    assert len(deck.cards) == 51
