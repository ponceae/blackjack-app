"""
Tests for the payout `calculator.py` module.

Contains tests for validating various Blackjack payout amounts, including:
- Natural blackjack (3:2).
- Standard win (1:1).
- Insurance win (2:1).
- Push (Return of original wager).
"""

__author__ = 'Adrien P.'

import pytest

from blackjack.bank import Bank
from blackjack.datatypes import Insurance, Player, PlayerHand
from blackjack import payout_calculator

@pytest.mark.parametrize(
    'test_wager, expected_payout',
    [
        (15.0, 37.5),
        (1000, 2500.0),
        (534.25, 1335.625),
    ]
)
def test_blackjack_payouts(test_wager, expected_payout):
    hand = PlayerHand(wager=test_wager)
    assert payout_calculator.blackjack_payout(hand) == expected_payout

def test_insurance_logic_and_bank_update_low_cost():
    insurance = Insurance(cost=7.5)
    player = Player(username='Test', bank=Bank(15.0))

    payout_calculator.insurance_logic(insurance, player)

    assert insurance.payout == 15.0
    assert player.bank.chips == 30.0

def test_insurance_logic_and_bank_update_high_cost():
    insurance = Insurance(cost=27.5)
    player = Player(username='Test', bank=Bank(25.0))

    payout_calculator.insurance_logic(insurance, player)

    assert insurance.payout == 55.0
    assert player.bank.chips == 80.0

@pytest.mark.parametrize(
    'test_wager, expected_cost',
    [
        (15, 7.5),
        (27.5, 13.5),
        (346.34, 173.0),
        (4635.32, 2317.5), 
    ]
)
def test_get_insurance_cost(test_wager, expected_cost):
    hand = PlayerHand(wager=test_wager)
    assert payout_calculator.get_insurance_cost(hand) == expected_cost

@pytest.mark.parametrize(
    'test_wager, expected_payout',
    [
        (15, 15.0),
        (345.75, 345.75),
    ]
)
def test_push_payout(test_wager, expected_payout):
    hand = PlayerHand(wager=test_wager)
    assert payout_calculator.push_payout(hand) == expected_payout

@pytest.mark.parametrize(
    'test_wager, expected_payout',
    [
        (15, 30.0),
        (345.75, 691.5),
    ]
)
def test_standard_win_payout(test_wager, expected_payout):
    hand = PlayerHand(wager=test_wager)
    assert payout_calculator.standard_payout(hand) == expected_payout
