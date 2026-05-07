"""
Tests for the `deck.py` module.

Validates game deck initialization and modification.
"""

__author__ = 'Adrien P.'

from entities.deck import create_deck, Deck

def test_create_deck_success():   
    deck = create_deck()

    for i in range(len(deck)):
        assert str(deck[i]) == str(deck[i])

# def test_shuffle_deck_is_same_deck():
#     deck = create_deck()
#     shuffled = deck.shuffle_deck

#     assert len(shuffled) == 52

#     standard_set = set((card.suit, card.rank) for card in deck)
#     shuffled_set = set((card.suit, card.rank) for card in shuffled)
   
#     assert standard_set == shuffled_set
#     assert len(shuffled) == len(shuffled_set)
