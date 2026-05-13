""" 
Tests for the `conditions.py` module.

Validates comparing game hands, the wager affordability of a player, and whether a 
player can purchase insurance.
"""

__author__ = 'Adrien P.'

import pytest

from engine import conditions
from data import conditions_data as cd
from entities import Player, Table

@pytest.fixture
def player():
    """Provide a `Player` instance with a moderate balance and an empty hand."""
    return Player()

@pytest.mark.parametrize(
    'player_hand, dealer_hand, expected_outcome',
    [
        (player, dealer, outcome) for (player, dealer, outcome, *_) 
        in cd.generate_initial_deal_outcome_data()
    ],
    ids=[tid[3] for tid in cd.generate_initial_deal_outcome_data()]
)
def test_compare_initial_hands(player_hand, dealer_hand, expected_outcome):
    table = Table(player=Player(hands=[player_hand]), dealer=dealer_hand)
    
    assert conditions.compare_initial_hands(table) == expected_outcome

@pytest.mark.parametrize(
    'player_hand, dealer_hand, expected_outcome',
    [
        (player, dealer, outcome) for (player, dealer, outcome, *_)
        in cd.generate_end_of_round_outcome_data()
    ],
    ids=[tid[3] for tid in cd.generate_end_of_round_outcome_data()]
)
def test_compare_end_of_round_hands(player_hand, dealer_hand, expected_outcome):
    assert conditions.compare_hands(player_hand, dealer_hand) == expected_outcome

@pytest.mark.parametrize(
    'wager_amount, expected_bool',
    [(-1, False), (500.01, False), (500, True), (499, True), (0, False)],
)
def test_validate_wager_and_is_valid_wager(player, wager_amount, expected_bool):
    assert conditions._validate_wager(player, wager_amount) == expected_bool
    assert conditions.is_valid_wager(player, wager_amount) == expected_bool

@pytest.mark.parametrize(
    'dealer_hand, expected_bool, wager_amount',
    [
        (dealer, cond, wager) for (dealer, cond, wager, *_) 
        in cd.generate_dealerhands_and_balances()
    ],
    ids=[tid[3] for tid in cd.generate_dealerhands_and_balances()]
)
def test_player_can_take_insurance(player, dealer_hand, expected_bool, wager_amount):
    table = Table(player=player, dealer=dealer_hand)
    
    assert conditions.can_take_insurance(table, wager_amount) == expected_bool
