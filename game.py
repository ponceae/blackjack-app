"""
Single-Deck Blackjack.
Dealer stands on soft 17.
Insurance offered.
"""

__author__ = 'Adrien P.'

import actions
from bank import Bank
import conditions
import constants
from datatypes import (
    Insurance,
    Outcome,
    Player,
    PlayerAction,
    PlayerHand,
    SplitHands,
    Table
)
import interface
import payout_calculator

# ==================================================
# INITIAL ROUND ACTIONS
# Player or dealer blackjack and insurance handling.
# ==================================================

def exe_initial_cond(table: Table) -> bool:
    """
    Execute the initial round deal check.

    Checks for a player or dealer blackjack (or a push if tied) after the initial 
    round deal is completed. The user is also prompted to purchase insurance if the 
    dealer is showing an Ace. If any of the above conditions apply, update the player's 
    bank balance accordingly depending on the win condition.

    Args:
        table (Table): The current game table containing the player and dealer hands.
    Returns:
        bool: `True` if the user wishes to start a new round, `False` otherwise.
    """  
    insurance, outcome = Insurance(), Outcome()

    player_hand = table.player.hands[0]

    outcome.flag = conditions.compare_initial_hands(table)
    
    _handle_insurance(insurance, table)
 
    if outcome.flag in (constants.PLAYER_WIN, constants.DEALER_WIN, constants.PUSH): 
        _handle_outcomes(outcome, insurance, table)

        interface.load_timer(constants.SHOW)

        table.dealer.is_hidden = False

        interface.clear_and_print(table) 

        table.player.hands[0].insurance_wager = 0

        interface.clear_and_print(table)
        interface.print_initial_insurance_outcome(insurance) 
        interface.print_initial_outcome(outcome, player_hand)

        if interface.is_new_round(table):
            return True

    if insurance.active: 
        # Player purchased insurance and lost.
        insurance.win = False
        table.player.hands[0].insurance_wager = 0

    interface.clear_and_print(table)
    interface.print_initial_insurance_outcome(insurance)

    return False

def _handle_insurance(insurance: Insurance, table: Table) -> None:
    """
    Prompt the user if they wish to purchase insurance. 

    Fetches the insurance cost and checks that the dealer is showing an Ace. If they 
    are, continually ask the user if they wish to purchase insurance until a valid 
    answer is given. If purchased, update the insurance status and the player's bank
    balance accordingly.

    Args:
        insurance (Insurance): The current player insurance state.
        table (Table): The current game table containing the player hand.
        player_hand (PlayerHand): The player's hand containing the wager.
    """
    insurance.cost = payout_calculator.get_insurance_cost(table.player.hands[0])

    player_hand = table.player.hands[0]

    if table.dealer.cards[0].rank == constants.ACE:
        interface.load_timer(constants.INITIAL)
        interface.clear_and_print(table)
        # Verify player has enough chips for insurance.
        if (interface.request_insurance(insurance.cost) == constants.YES):
            if conditions.is_valid_insurance_wager(table.player, player_hand):  
                insurance.active = True

                player_hand.insurance_wager = insurance.cost
                table.player.bank.chips -= insurance.cost

                interface.clear_and_print(table)
            else:
                interface.clear_and_print(table)
                interface.load_timer(constants.BROKE)

def _handle_outcomes(outcome: Outcome, insurance: Insurance, table: Table) -> None:
    """
    Check for an initial win condition.

    Checks for a player or dealer blackjack, or both and depending on the win 
    condition updates the player bank balance with the correct payout and insurance if
    purchased and won.

    Args:
        outcome (Outcome): The current game state win condition.
        insurance (Insurance): The current player insurance state.
        table (Table): The current game table containing the player and dealer hands.
    """
    player_hand = table.player.hands[0]

    # Dealer blackjack, hidden card is shown.
    if outcome.flag == constants.DEALER_WIN:
        interface.clear_and_print(table)
        # Payout insurance to the player.
        _insurance_helper(insurance, table)
    # Return initial wager to the player.
    elif outcome.flag == constants.PUSH:
        outcome.payout = payout_calculator.push_payout(player_hand)
        table.player.bank.chips += outcome.payout
        # Even money payout.
        _insurance_helper(insurance, table)
    elif outcome.flag == constants.PLAYER_WIN:
        outcome.payout = payout_calculator.blackjack_payout(player_hand)
        table.player.bank.chips += outcome.payout

def _insurance_helper(insurance: Insurance, table: Table) -> None:
    """
    Update the player bank if insurance was purchased and won.

    Args:
        insurance (Insurance): The current player insurance state.
        table (Table): The current game table containing the player and dealer hands.
    """
    if insurance.active:
        insurance.win = True
        payout_calculator.insurance_logic(insurance, table.player)

# ==================================================
# PLAYER TURN ACTIONS
# Player can hit, stand, split, or double down.
# ==================================================

def exe_player_control(table: Table) -> None:
    """
    Execute the player turn.

    If the player contains cards of equal rank on the initial deal, continually prompt
    them if they wish to split until a valid answer is given. If the player is given
    split aces, end the turn. Then iterate through each player hand and continually
    ask the user if they wish to double down until a valid answer is given. Then 
    continually ask the user if they wish to hit until they wish to stand or a round
    ending condition is met. Updates the player bank balance and player hands 
    accordingly.

    Args:
        table (Table): The current game table containing the player hands.
    """
    split = SplitHands()
    _handle_split(table, split)

     # Cannot hit on split aces, advance to the dealer's turn.
    if split.split_aces:
        return

    interface.clear_terminal()
     
    for i, hand in enumerate(table.player.hands):
        table.player.hands[i].is_active = True

        interface.print_hands(table)

        # User can only double down before hitting.
        try:
            ans = interface.double_or_not()
            if (
                ans == constants.YES 
                and conditions.is_valid_doubled_wager(
                    table.player, 
                    table.player.hands[i],
                )
            ):
                action = _handle_double_down(table, i, split)

                if action == PlayerAction.NEXT_HAND:
                    continue
                else:
                    break
            elif (
                ans == constants.YES
                and not conditions.is_valid_doubled_wager(
                    table.player,
                    table.player.hands[i],
                )
            ):
                interface.load_timer(constants.BROKE)
                interface.clear_and_print(table)

            interface.clear_and_print(table)

            action = _handle_hitting(table, split, hand, i)
            
            if action == PlayerAction.NEXT_HAND:
                    continue

        finally:
            table.player.hands[i].is_active = False

def _handle_hitting(
    table: Table,
    split: SplitHands,
    hand: PlayerHand,
    i: int
) -> PlayerAction:
    """
    Handle the player hitting for a card at the table.

    Continually prompt the user if they wish to hit or stand on the current hand until
    a valid answer is given. Adds a new card to the player's hand and checks if
    a bust or twenty one occured and if there are still hands left to hit or stand. 
    Main loop when a player decides to hit the current hand. Returns the next 
    player action based off of their decision.

    Args:
        table (Table): The current game table containing the player hands
        split (SplitHands): The current player's split hand status.
        hand (PlayerHand): The current player's hand.
        i (int): The current player's hand pointer.
    Returns:
        PlayerAction: The next player action.
    """
    while interface.hit_or_stand() == constants.HIT:
        actions.hit_hand(table, hand)

        interface.clear_and_print(table)

        if conditions.is_bust(hand):
            interface.print_stand_or_bust(i, constants.BUST)

            if _hands_left(split, table.player.hands, i):
                return PlayerAction.NEXT_HAND
            else:
                return PlayerAction.END_TURN

        elif conditions.is_twenty_one(hand):
            interface.print_stand_or_bust(i, constants.STAND)

            if _hands_left(split, table.player.hands, i):
                return PlayerAction.NEXT_HAND
            else:
                return PlayerAction.END_TURN

    if _hands_left(split, table.player.hands, i):
        return PlayerAction.NEXT_HAND
    else:
        return PlayerAction.END_TURN

def _hands_left(split: SplitHands, player_hands: list[PlayerHand], i: int) -> bool:
    """
    Check the state of the current player's hand and return `True` if the player
    has more hands left to play.

    Args:
        split (SplitHands): The current player's split hand status.
        player_hands (list[PlayerHand]): The player's current hands at the table.
        i (int): The current player's hand pointer.

    Returns:
        bool: `True` if the player has another hand left to play, `False` otherwise.
    """
    # Switch hands if applicable.
    if (split.split_hand and i != len(player_hands) - 1): 
        interface.load_timer(constants.PLAYER)
        interface.clear_terminal()
        return True

    # Normal flow, player turn is finished.
    interface.load_timer(constants.SWITCH_TURN) 
    interface.clear_terminal()

    return False

def _handle_double_down(table: Table, i: int, split: SplitHands) -> PlayerAction:
    """
    Update the player bank and add a card to the player's hand. Check if another
    hand is left to play and return the next player action.

    Args: 
        table (Table): The current game table containing the player hands.
        i (int): The current player's hand pointer.
        split (SplitHands): The current player's split hand status.

    Returns:
        PlayerAction: The player action.
            - 1: `NEXT_HAND`
            - 2: `END_TURN`
    """
    table.player.bank.chips -= table.player.hands[i].wager

    table.player.hands[i].wager += table.player.hands[i].wager

    actions.hit_hand(table, table.player.hands[i]) 

    interface.clear_and_print(table)

    if _hands_left(split, table.player.hands, i): 
        # Switch player hands if applicable.
        return PlayerAction.NEXT_HAND 
    else:
        return PlayerAction.END_TURN

def _handle_split(table: Table, split: SplitHands) -> None:
    """
    Add a new hand to the player's current hands and update the player bank.

    Continually prompt the user if they wish to split their current hand until a 
    valid answer is given. If the user can afford to split their hand, adds a hand 
    to the player and updates's the player's bank balance with the wager equal to the 
    amount of their initial wager.

    Args:
        table (Table): The current game table containing the player hands.
        split (SplitHands): The current player's split hand status.
    """
    req_split = (
        conditions.can_split(table.player.hands[0]) 
        and interface.split_or_not() == constants.YES
    )

    if (
        req_split
        and conditions.is_valid_doubled_wager(table.player, table.player.hands[0])
    ): 
        # User wishes to split & has enough chips.
        split.split_hand = True 

        split_aces = conditions.is_split_aces(table.player.hands[0])
        
        actions.create_split_hands(table)

        table.player.bank.chips -= table.player.hands[0].wager
        table.player.hands[1].wager = table.player.hands[0].wager

        if split_aces:
            split.split_aces = True

    elif (
        req_split 
        and not conditions.is_valid_doubled_wager(table.player, table.player.hands[0])
    ):
        interface.load_timer(constants.BROKE)

# ======================
# DEALER TURN ACTIONS.
# ======================

def exe_dealer_control(table: Table) -> None:
    """
    Execute the dealer turn. 

    The dealer hits until they encounter a soft 17 in which case the turn ends.

    Args:
        table (Table): The current game table containing the dealer hand.
    """
    interface.print_hands(table)
    # Dealer will now show the hidden card
    interface.load_timer(constants.SHOW) 

    table.dealer.is_hidden = False
    
    interface.clear_and_print(table)
    
    while actions.get_hand_value(table.dealer) < 17: 
        interface.load_timer(constants.DEALER) 
        
        actions.hit_hand(table, table.dealer) 
        
        interface.clear_and_print(table)
        
        if conditions.is_bust(table.dealer):
            interface.print_dealer_state(constants.BUST)
            return
        elif conditions.is_twenty_one(table.dealer):
            interface.print_dealer_state(constants.STAND)
            return
        
    interface.print_dealer_state(constants.STAND)

# ==================
# ROUND END CHECK.
# ==================

def verify_round_end_cond(table: Table) -> bool:
    """
    Compare the hand values at the end of the round and determine the winner.

    Iterates through all of the player's hands and compares them to the dealer's hand.
    If a winner is found the player's bank balance is updated and the round outcome
    message is displayed. 

    Args:
        table (Table): The current game table containing the player and dealer hands.
    """
    tmp_buffer = []
    
    outcome = Outcome()
    
    dealer_bust = conditions.is_bust(table.dealer)
    
    table.dealer.is_hidden = False
    
    interface.print_hands(table)
    
    for i, hand in enumerate(table.player.hands):
        player_bust = conditions.is_bust(hand)
        
        if player_bust:
            tmp_buffer.append(interface.get_round_outcome_msg(i, constants.BUST))
            # Check next hand if applicable or exit on a bust.
            continue 
        elif not player_bust and dealer_bust:
            table.player.bank.chips += payout_calculator.standard_payout(hand)
            
            tmp_buffer.append(interface.get_round_outcome_msg(i, constants.WIN))
            tmp_buffer.append(interface.get_round_outcome_payout_msg(hand))
        elif not player_bust and not dealer_bust: 
            msg, outcome.flag = interface.compare_hands(table, hand, i)
            
            tmp_buffer.append(msg)
            
            if outcome.flag == constants.PUSH:
                table.player.bank.chips += payout_calculator.push_payout(hand)
            elif outcome.flag == constants.PLAYER_WIN:
                table.player.bank.chips += payout_calculator.standard_payout(hand)
    
    interface.clear_and_print(table)
    
    for strings in tmp_buffer:
        print(*strings, sep='', end='')
    if interface.is_new_round(table):
        return True
    return False

def _get_player_wager(table: Table) -> float:
    """
    Prompt the user for a wager amount and update the player's bank balance.

    Args:
        player (Player): The player whose wager is being set.

    Returns:
        float: The player's wager amount.
    """
    wager = interface.wager_prompt(table) 

    interface.clear_terminal()

    table.player.bank.chips -= wager 

    return wager

def blackjack(deck: list, player_bank: Bank, username: str) -> None:
    """
    Execute the main blackjack game loop.

    Continually execute the initial round deal, the player turn, the dealer turn,
    and restart the round until the user runs out of chips or chooses to end the 
    game.

    Args:
        deck (list): The current game table's deck of cards.
        player_bank (Bank): The current player's bank balance.
    """
    table = Table(Player(username=username, bank=player_bank))
    table.deck = deck

    while True:
        wager_amount = _get_player_wager(table)

        round_done = False

        actions.initial_round_deal(table)
        table.player.hands[0].wager = wager_amount

        interface.print_hands(table)

        round_done = round_done or exe_initial_cond(table)	

        if not round_done:
            exe_player_control(table)
            exe_dealer_control(table)

            interface.load_timer(constants.CHECK)
            interface.clear_terminal()

            round_done = verify_round_end_cond(table)

        if not round_done:
            break

def main():
    """
    Start the Blackjack game. Initialize the player bank and begin the main 
    game loop.
    """
    print(
            f'Blackjack Pays 3:2\n'
            f'Dealer Stands on Soft 17\n'
            f'Insurance Pays 2:1\n'
        )
    input('Press Enter to Continue\n>')

    interface.clear_terminal()

    # chips, username = storage.pull_user_info()
    # player_bank = Bank(chips)

    interface.clear_terminal()

    # blackjack(actions.create_and_shuffle(), player_bank, username)

if __name__ == '__main__':
    main()
