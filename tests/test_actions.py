""" 
Tests for the `actions.py` module.

Validates hand values, ensures that hitting and splitting hands adds the correct
amount of cards to the hand, and that only two cards are dealt at the beginning
of the round.
"""

__author__ = 'Adrien P.'

import pytest

from blackjack.card import Card
from blackjack import actions
from blackjack.datatypes import Hand, Player, PlayerHand, Table

def _generate_test_cards() -> list[list[Card]]:
    """Provide a list of hands in order to test their values."""
    return [
        [Card('Clubs', 2), Card('Hearts', 3), Card('Spades', 4)],
        [Card('Clubs', 10), Card('Hearts', 'Jack')],
        [Card('Clubs', 7), Card('Hearts', 8), Card('Spades', 9)],
        [Card('Clubs', 'Ace'), Card('Hearts', 5)],
        [Card('Clubs', 'Ace'), Card('Spades', 'King')],
        [Card('Clubs', 'Ace'), Card('Hearts', 2), Card('Spades', 3)],
        [Card('Clubs', 2), Card('Hearts', 9), Card('Spades', 'Ace')],
        [Card('Clubs', 'Ace'), Card('Hearts', 'Ace')],
        [Card('Clubs', 'Ace'), Card('Hearts', 'Ace'), Card('Spades', 9)],
        [Card('Clubs', 'Ace'), Card('Hearts', 'Ace'), Card('Spades', 'King')],
        [
            Card('Clubs', 'Ace'), 
            Card('Hearts', 'Ace'), 
            Card('Spades', 'Ace'), 
            Card('Diamonds', 'Ace'),
        ],
        [Card('Clubs', 'Ace'), Card('Hearts', 9)],
        [Card('Clubs', 'Ace'), Card('Hearts', 4), Card('Spades', 6)],
        [Card('Clubs', 'Ace'), Card('Hearts', 5), Card('Spades', 6)],
    ]

def _generate_expected_values(flag) -> list[int]:
    """
    Provide a list of expected values for the `_generate_test_cards()` function 
    depending on the type of test.
    """
    if flag == 'optimal':
        return [9, 20, 24, 16, 21, 16, 12, 12, 21, 12, 14, 20, 21, 12]
    elif flag == 'hard':
        return [9, 20, 24, 6, 11, 6, 12, 2, 11, 12, 4, 10, 11, 12]
    return []

def _generate_test_ids() -> list[str]:
    """
    Provide test ID's for the `_generate_test_cards() and 
    `_generate_expected_values()` functions.
    """
    return [
        'two_pip_cards',
        'one_pip_one_face_card',
        'three_pips',
        'ace_one_pip_card_a',
        'ace_one_pip_one_face_card',
        'ace_two_pip_cards_a',
        'ace_two_pip_cards_b',
        'two_aces',
        'two_aces_one_pip_card',
        'two_aces_one_face_card',
        'four_aces',
        'ace_one_pip_card_b',
        'ace_two_pip_cards_c',
        'ace_two_pip_cards_d',
    ]

@pytest.mark.parametrize(
    'test_cards, expected_value',
    zip(_generate_test_cards(), _generate_expected_values('optimal')),   
    ids=_generate_test_ids()
)
def test_optimal_hand_values(test_cards, expected_value):
    hand = Hand(cards=test_cards)
    assert actions.get_hand_value(hand) == expected_value

@pytest.mark.parametrize(
    'test_cards, expected_value',
    zip(_generate_test_cards(), _generate_expected_values('hard')),
    ids=_generate_test_ids()
)
def test_hard_hand_values(test_cards, expected_value):
    hand = Hand(cards=test_cards)
    assert actions.get_hard_value(hand) == expected_value

@pytest.fixture
def table() -> Table:
    """Provide a `Table` instance preloaded with a deck."""
    return Table(player=Player(username='Test'), deck=actions.create_and_shuffle())

def test_create_split_hands_created_new_hand(table):
    table.player.hands = [PlayerHand(cards=[Card('Clubs', 6), Card('Hearts', 6)])]

    actions.create_split_hands(table)

    assert len(table.player.hands) == 2

    assert table.player.hands[0].cards[0].to_string() == '♣6'
    assert table.player.hands[1].cards[0].to_string() == '♥6'

def test_hit_hand_added_card_to_hand(table):
    table.player.hands = [PlayerHand(cards=[Card('Clubs', 4), Card('Hearts', 6)])]
    actions.hit_hand(table, table.player.hands[0])

    assert len(table.player.hands[0].cards) == 3

def test_hit_hand_continues_after_empty_deck(table):
    table.player.hands = [PlayerHand(cards=[])]    
    table.deck.clear()

    actions.hit_hand(table, table.player.hands[0])

    assert len(table.player.hands[0].cards) == 1

def test_initial_round_dealt_correct_num_cards_to_hands(table):
    actions.initial_round_deal(table)

    assert len(table.player.hands) == 1
    assert len(table.player.hands[0].cards) == 2

    assert len(table.dealer.cards) == 2

def test_initial_round_deal_success_on_empty_deck(table):
    table.deck.clear()
    actions.initial_round_deal(table)

    assert len(table.player.hands) == 1
    assert len(table.player.hands[0].cards) == 2

    assert len(table.dealer.cards) == 2

def test_create_and_shuffle_created_new_deck():
    deck = actions.create_and_shuffle()
    assert len(deck) == 52
