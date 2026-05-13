"""
Blackjack game state validators.

Evaulates game hands and validates player wagers.
"""

__author__ = 'Adrien P.'

from constants import ACE
from entities import DealerHand, Outcome, OutcomeFlag, Player, PlayerHand, Table

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

def compare_hands(player_hand: PlayerHand, dealer_hand: DealerHand) -> Outcome:
    """ 
    Compare the hands at the end of the round and return the outcome.
    
    Args:
        player_hand (PlayerHand): The player's hand to evaluate.
        dealer_hand (DealerHand): The dealer's hand to evaluate.s
        
    Returns:
        Outcome: The outcome after the round has finished.
    """
    player_score = player_hand.value
    dealer_score = dealer_hand.value
    
    outcome = Outcome()
    
    if player_score == dealer_score:
        outcome.flag = OutcomeFlag.PUSH
    elif player_score > dealer_score:
        outcome.flag = OutcomeFlag.PLAYER_WIN
    elif player_score < dealer_score:
        outcome.flag = OutcomeFlag.DEALER_WIN
        
    return outcome

def _validate_wager(player: Player, amount: float) -> bool:
    """
    Return `True` if the provided amount is positive and the player can afford it, 
    `False` otherwise.
    
    Args:
        player (Player): The player attempting to place a wager.
        amount (float): The amount of the wager.
    
    Returns:
        bool: `True` if the amount is positive and the player can afford it, `False`
            otherwise.
    """
    if amount <= 0 or not player.can_afford(amount):
        return False

    return True

def is_valid_wager(player: Player, amount: float) -> bool:
    """
    Return `True` if the player can afford to place a wager of the provided amount.
    
    Args:
        player (Player): The player attempting to place a wager.
        amount (float): The amount of the wager.
        
    Returns:
        bool: `True` if the player can afford to place the wager, `False` otherwise.
    """
    return _validate_wager(player, amount)

def can_take_insurance(table: Table, amount: float):
    """ 
    Return `True` if the dealer is showing an Ace and the player can afford insurance.
    
    Args:
        table (Table): The current game table containing the player's and dealer's 
            hand.
        amount (float): The cost for purchasing insurance.
        
    Returns:
        bool: `True` if the player can afford to purchase insurance, `False`
            otherwise.
    """
    if table.dealer.cards[0].rank != ACE:
        return False
    
    return is_valid_wager(table.player, amount)
