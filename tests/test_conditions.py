""" 
Tests for the `conditions.py` module.

Validates various game, hand, and player states.
"""

__author__ = 'Adrien P.'

import pytest

from entities.bank import Bank
from entities.card import Card
import conditions
import constants
from datatypes import Player, Table
from entities.hand import DealerHand, Hand, PlayerHand

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    [
        ([Card('Clubs', 8), Card('Hearts', 8)], True),
        ([Card('Spades', 'Ace'), Card('Diamonds', 'Ace')], True),
        ([Card('Hearts', 'King'), Card('Clubs', 'Queen')], False),
        ([Card('Hearts', 9), Card('Clubs', 4)], False),
    ],
    ids=[
        'can_split_a',
        'can_split_b',
        'cannot_split_a',
        'cannot_split_b',  
    ],
)
def test_can_split_hand(test_cards, expected_bool):
    hand = Hand(cards=test_cards)
    assert conditions.can_split(hand) == expected_bool

@pytest.mark.parametrize(
    'player_cards, dealer_cards, expected_flag',
    [
        (
            [Card('Clubs', 'Ace'), Card('Hearts', 10)], 
            [Card('Spades', 'Ace'), Card('Diamonds', 10)], 
            constants.PUSH
        ),
        (
            [Card('Clubs', 'Ace'), Card('Hearts', 10)],
            [Card('Spades', 2), Card('Diamonds', 10)],
            constants.PLAYER_WIN,
        ),
        (
            [Card('Clubs', 2), Card('Hearts', 10)],
            [Card('Spades', 'Ace'), Card('Diamonds', 10)],
            constants.DEALER_WIN,
        ),
        (
            [Card('Clubs', 2), Card('Hearts', 10)],
            [Card('Spades', 4), Card('Diamonds', 10)],
            0,
        ),
    ],
    ids=[
        'test_initial_push',
        'test_initial_player_win',
        'test_initial_dealer_win',
        'test_no_initial_outcome',
    ],
)
def test_initial_hands_outcome_flags_match(player_cards, dealer_cards, expected_flag):
    table = Table(
        player=Player(
            username='Test',
            hands=[PlayerHand(cards=player_cards)]
        ),
        dealer=DealerHand(cards=dealer_cards)
    )

    assert conditions.compare_initial_hands(table) == expected_flag

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    [
        ([Card('Clubs', 8), Card('Hearts', 8), Card('Diamonds', 8)], True),
        ([Card('Spades', 'Ace'), Card('Diamonds', 5)], False),
        ([Card('Spades', 10), Card('Clubs', 5), Card('Hearts', 10)], True),
        ([Card('Hearts', 'Ace'), Card('Clubs', 'Ace'), Card('Spades', 10)], False),
        (
            [
                Card('Clubs', 3), 
                Card('Hearts', 4), 
                Card('Spades', 7), 
                Card('Clubs', 4),
            ], 
            False
        ),
    ],
    ids=[
        'three_card_bust_a',
        'ace_two_card_nonbust',
        'three_card_bust_b',
        'two_ace_three_card_nonbust',
        'four_card_nonbust',
    ],
)
def test_hand_is_bust_or_not(test_cards, expected_bool):
    hand = Hand(cards=test_cards)
    assert conditions.is_bust(hand) == expected_bool

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    [
        ([Card('Clubs', 8), Card('Hearts', 4)], False),
        ([Card('Spades', 'Ace'), Card('Diamonds', 5)], True),
    ],
    ids=[
        'is_not_soft_a',
        'is_soft_a',
    ],
)
def test_hand_is_soft_or_not(test_cards, expected_bool):
    hand = Hand(cards=test_cards)
    assert conditions.is_soft(hand) == expected_bool

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    [
        ([Card('Clubs', 'Ace'), Card('Hearts', 'Ace')], True),
        ([Card('Spades', 5), Card('Diamonds', 5)], False),
        ([Card('Clubs', 8), Card('Hearts', 10)], False),
    ],
    ids=[
        'is_split_ace_hand_a',
        'not_split_ace_hand_a',
        'not_split_ace_hand_b',
    ],
)
def test_hand_has_split_aces_or_not(test_cards, expected_bool):
    hand = Hand(cards=test_cards)
    assert conditions.is_split_aces(hand) == expected_bool

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    [
        ([Card('Clubs', 7), Card('Hearts', 8), Card('Clubs', 6)], True),
        ([Card('Spades', 5), Card('Diamonds', 10)], False),
    ],
    ids=[
        'hand_is_twenty_one_a',
        'hand_not_twenty_one_b',
    ],
)
def test_is_hand_twenty_one(test_cards, expected_bool):
    hand = Hand(cards=test_cards)
    assert conditions.is_twenty_one(hand) == expected_bool

@pytest.fixture
def player():
    """Provide a `Player` instance with minimal chips."""
    return Player(username='Test', bank=Bank(25.0)) 

@pytest.mark.parametrize(
    'chips, expected_bool',
    [
        (constants.MIN_WAGER, True),
        (constants.MAX_WAGER, True),
        (constants.MIN_WAGER - 0.01, False),
        (constants.MAX_WAGER + 0.01, False),
        (500, True),
        (27.5, True),
        (-33.6, False),
    ],
    ids=[
        'valid_bounds_a',
        'valid_bounds_b',
        'invalid_bounds_a_small',
        'invalid_bounds_b_big',
        'valid_bounds_c',
        'valid_bounds_d',
        'invalid_bounds_c_negative'
    ]
)
def test_is_valid_chip_bounds(chips, expected_bool):
    assert conditions.is_valid_chip_bounds(chips) == expected_bool

@pytest.mark.parametrize(
    'chips, expected_bool',
    [
        (15, True),
        (27.5, True),
        (14.99, False),
        (0, False),
        (-4.3, False),
        (5, False),
    ],
    ids=[
        'valid_wager_a',
        'valid_wager_b',
        'invalid_wager_a_small',
        'invalid_wager_b_zero',
        'invalid_wager_c_negative',
        'invalid_wager_d_small',
    ]
)
def test_is_valid_wager(chips, expected_bool):
    assert conditions.is_valid_wager(chips) == expected_bool

@pytest.mark.parametrize(
    'test_wager, expected_bool',
    [
        (15.0, True),
        (10, False),
        (16, True),
    ],
    ids=[
        'valid_wager_a',
        'invalid_wager_a_small',
        'valid_wager_b',
    ]
)
def test_verify_min_bet(test_wager, expected_bool):
    player_hand = PlayerHand(wager=test_wager)  
    assert conditions.is_valid_hand_wager(player_hand) == expected_bool

@pytest.mark.parametrize(
    'wager, expected_bool',
    [
        (15.0, True),
        (35, True),
        (-3.2, False),
        (0, False),
        (14.99, False),
    ],
    ids=[
        'valid_wager_a',
        'valid_wager_b',
        'invalid_wager_a_negative',
        'invalid_wager_b_zero',
        'invalid_wager_c_small',
    ]
)
def test_is_valid_player_wager(player, wager, expected_bool):
    assert conditions.is_valid_player_wager(player, wager) == expected_bool

@pytest.mark.parametrize(
    'chips, test_wager, expected_bool',
    [
        (50.0, 25.0, True),
        (25.0, 50.0, False),
        (0.0, 50.0, False),
    ],
    ids=[
        'valid_wager_a',
        'invalid_wager_a_broke',
        'invalid_wager_b_broke',
    ]
)
def test_is_valid_doubled_wager(chips, test_wager, expected_bool):
    player = Player(username='Test', bank=Bank(chips))
    player_hand = PlayerHand(wager=test_wager)   

    assert conditions.is_valid_doubled_wager(player, player_hand) == expected_bool 

@pytest.mark.parametrize(
    'chips, test_wager, expected_bool',
    [
        (25.0, 15.0, True),
        (5.0, 15.0, False),
    ],
    ids=[
        'valid_wager_a',
        'invalid_wager_a_broke',
    ]
)
def test_is_valid_insurance_wager(chips, test_wager, expected_bool):
    player = Player(username='Test', bank=Bank(chips))
    player_hand = PlayerHand(wager=test_wager)

    assert conditions.is_valid_insurance_wager(player, player_hand) == expected_bool
