# """
# Blackjack game state validators and checks.

# This module contains functions for checking hand and game states, as well as 
# player bank statuses.
# """

__author__ = 'Adrien P.'

# from constants import ACE, DEALER_WIN, MAX_WAGER, MIN_WAGER, PLAYER_WIN, PUSH
# from datatypes import Player, Table
# from entities.hand import Hand, PlayerHand
# from engine.payout_calculator import get_insurance_cost

from entities import Outcome, OutcomeFlag, Table

def compare_initial_hands(table: Table) -> Outcome:
    """
    Compare the hands at the start of the round and return the outcome.

    Args:
        table (Table): The table containing the player's and dealer's hands.

    Returns:
        Outcome: The outcome after the initial cards have been dealt.
    """
    player_blackjack = table.player.hands[0].is_twenty_one
    dealer_blackjack = table.dealer.is_twenty_one

    outcome = Outcome()

    if player_blackjack and dealer_blackjack:
        outcome.flag = OutcomeFlag.PUSH
    elif player_blackjack and not dealer_blackjack:
        outcome.flag = OutcomeFlag.PLAYER_BLACKJACK
    elif not player_blackjack and dealer_blackjack:
        outcome.flag = OutcomeFlag.DEALER_BLACKJACK

    return outcome

# def is_valid_wager(wager: float) -> bool:
#     """Return `True` if the wager is greater than or equal to the `MIN_WAGER`."""
#     return wager >= MIN_WAGER

# def is_valid_hand_wager(hand: PlayerHand) -> bool:
#     """
#     Return `True` if the hand's current wager meets the required `MIN_WAGER`.

#     Args:
#         hand (PlayerHand): The hand containing the wager.
    
#     Returns:
#         bool: `True` if the hand meets the `MIN_WAGER`, `False` otherwise.
#     """
#     return is_valid_wager(hand.wager)

# def is_valid_player_wager(player: Player, wager: float) -> bool:
#     """
#     Return `True` if the wager meets at least the `MIN_WAGER`, and the player 
#     has enough chips to cover it.

#     Args:
#         player (Player): The player whose bank chips are being checked.
#         wager (float): The wager to check against.

#     Returns:
#         bool: `True` if the wager is valid and affordable, `False` otherwise.
#     """
#     if not is_valid_wager(wager):
#         return False

#     return is_valid_wager(player.bank.balance)

# def is_valid_chip_bounds(chips: float) -> bool:
#     """
#     Return `True` if the given chips fall within the valid range of 
#     `MIN_WAGER` to `MAX_WAGER` (inclusive).

#     Args:
#         chips (float): The chip balance to validate.
#     Returns:
#         bool: `True` if the chips are within bounds, `False` otherwise.
#     """
#     return isinstance(chips, (int, float)) and MIN_WAGER <= chips <= MAX_WAGER

# def is_valid_doubled_wager(player: Player, hand: PlayerHand) -> bool:
#     """ 
#     Return `True` if the player can afford to double their wager.

#     Args:
#         player (Player): The player whose bank chips are being checked.
#         hand (PlayerHand): The hand containing the wager.

#     Returns:
#         bool: `True` if the player can afford it, `False` otherwise.
#     """
#     return player.bank.balance >= hand.wager

# def is_valid_insurance_wager(player: Player, hand: PlayerHand) -> bool: 
#     """
#     Return `True` if the player can afford to purchase insurance.

#     Args:
#         player (Player): The player whose bank chips are being checked.
#         hand (PlayerHand): The hand containing the wager.

#     Returns:
#         bool: `True` if the player can afford it, `False` otherwise.
#     """
#     return get_insurance_cost(hand) <= player.bank.balance
