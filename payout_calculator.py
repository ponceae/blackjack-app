""" 
Blackjack payout functions.

This module contains functions for calculating the payouts for a blackjack, 
insurance, and double down win as well as returning the wager on a push.
"""

__author__ = 'Adrien P.'

import math

from .datatypes import Insurance, Player, PlayerHand

def blackjack_payout(hand: PlayerHand) -> float:
    """
    Return the payout for a natural blackjack win with 3:2 odds.

    Args: 
        hand (PlayerHand): The hand containing the wager.

    Returns:
        float: The blackjack payout.
    """
    return hand.wager * 2.5

def insurance_logic(insurance: Insurance, player: Player) -> None:
    """
    Calculate the insurance payout and add it to the player's bank.

    Args:
        insurance (Insurance): The active insurance data containing the wager cost.
        player (Player): The player receiving the payout.
    """
    insurance.payout = insurance_payout(insurance.cost)
    player.bank.chips += insurance.payout

def insurance_payout(insurance_cost: float) -> float:
    """
    Return the insurance payout with 2:1 odds.

    Args:
        insurance_cost (float): The cost of purchasing insurance.

    Returns:
        float: The insurance payout.
    """
    return insurance_cost * 2.0

def get_insurance_cost(hand: PlayerHand) -> float:
    """
    Return the cost for purchasing insurance.

    Args:
        hand (PlayerHand): The hand containing the wager.

    Returns:
        float: The insurance cost.
    """
    return math.floor(hand.wager) * 0.5

def push_payout(hand: PlayerHand) -> float:
    """
    Return the payout amount for a push (tied hand).

    Args:
        hand (PlayerHand): The hand containing the wager.

    Returns:
        float: The original wager.
    """
    return hand.wager

def standard_payout(hand: PlayerHand) -> float:
    """
    Return the payout for a standard win with 1:1 odds.

    Args:
        hand (PlayerHand): The hand containing the wager.

    Returns:
        float: The standard payout.
    """
    return hand.wager * 2.0
