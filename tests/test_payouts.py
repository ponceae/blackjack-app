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

from engine import payouts
from entities import PlayerHand

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
    
    assert payouts.blackjack_payout(hand) == expected_payout

@pytest.mark.parametrize(
    'test_wager, expected_cost, expected_payout',
    [
        (15.0, 7.5, 15.0),
        (25.0, 12.5, 25.0),
        (35.0, 17.5, 35.0),
        (45.0, 22.5, 45.0),
    ]
)
def test_insurance_payout_and_cost(test_wager, expected_cost, expected_payout):
    hand = PlayerHand(wager=test_wager)
    
    assert payouts.get_insurance_cost(hand) == expected_cost
    assert payouts.insurance_payout(expected_cost) == expected_payout

@pytest.mark.parametrize(
    'test_wager, expected_payout',
    [
        (15, 15.0),
        (345.75, 345.75),
    ]
)
def test_push_payout(test_wager, expected_payout):
    hand = PlayerHand(wager=test_wager)
    
    assert payouts.push_payout(hand) == expected_payout

@pytest.mark.parametrize(
    'test_wager, expected_payout',
    [
        (15, 30.0),
        (345.75, 691.5),
    ]
)
def test_standard_win_payout(test_wager, expected_payout):
    hand = PlayerHand(wager=test_wager)
    
    assert payouts.standard_payout(hand) == expected_payout
