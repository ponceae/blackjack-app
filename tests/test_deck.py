"""
Tests for the `deck.py` module.

Validates game deck initialization and modification.
"""

__author__ = 'Adrien P.'

from blackjack.deck import create_deck, shuffle_deck

def test_create_deck_success():   
    deck = create_deck()

    for i in range(len(deck)):
        assert deck[i].to_string() == deck[i].to_string()

def test_shuffle_deck_is_same_deck():
    deck = create_deck()
    shuffled = shuffle_deck(deck)

    assert len(shuffled) == 52

    standard_set = set((card.suit, card.rank) for card in deck)
    shuffled_set = set((card.suit, card.rank) for card in shuffled)
   
    assert standard_set == shuffled_set
    assert len(shuffled) == len(shuffled_set)
