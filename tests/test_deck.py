"""
Tests for the `deck.py` module.

Validates game deck initialization and modification.
"""

__author__ = 'Adrien P.'

import pytest

from entities.deck import  Deck

@pytest.fixture
def deck():
    return Deck()

def test_create_deck_has_52_cards(deck):   
    assert len(deck.cards) == 52

def test_shuffle_deck_is_same_deck(deck):
    deck.shuffle()

    assert len(deck.cards) == 52

def test_reset_is_new_deck(deck):
    deck.draw_card()
    deck.reset()

    assert len(deck.cards) == 52

def test_draw_card_removes_one(deck):
    deck.draw_card()
    assert len(deck.cards) == 51