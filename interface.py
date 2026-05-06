""" 
Blackjack display functions.

This module contains functions for the Blackjack CLI display, including:
- Displaying player and dealer hands
- Displaying round states,
- Prompting the user for input
"""

__author__ = 'Adrien P.'

import subprocess
import sys
import time

from actions import get_hand_value, get_hard_value
from entities.bank import Bank
from conditions import (
    is_soft, 
    is_twenty_one, 
    is_valid_player_wager, 
    is_valid_chip_bounds, 
    is_valid_wager,
)
from constants import (
    BUST,
    DEALER_WIN, 
    HIT, 
    MAX_WAGER,
    MIN_WAGER,
    NO, 
    PLAYER_WIN, 
    PUSH, 
    ROMAN_NUMERALS, 
    STAND, 
    TIMER_MESSAGES, 
    YES,
)
from datatypes import (
    Buffers,
    Insurance,
    Outcome,
    PlayerHand,
    Table,
)
from payout_calculator import push_payout, standard_payout

# ============================
# DISPLAY
# Main CLI display functions.
# ============================

def compare_hands(table: Table, hand: PlayerHand, index: int) -> tuple[str, int]:
    """
    Compare the player's hand against the dealer's to determine the outcome.

    Args:
        table (Table): The table containing the player and dealer hands.
        hand (PlayerHand): The current player hand being evaluated.
        index (int): The index of the current player hand.

    Returns:
        tuple[str, int]: A tuple containing:
            - str: The message displaying the flag outcome.
            - int: The flag representing the outcome type.
    """
    msg = 'Hand ' + ROMAN_NUMERALS[index + 1]

    player_hand_value = get_hand_value(hand)
    dealer_hand_value = get_hand_value(table.dealer)

    if player_hand_value == dealer_hand_value:
        return (f'{msg} Push, Returned ${push_payout(hand):,.2f}\n'), PUSH
    elif player_hand_value > dealer_hand_value:
        return (f'{msg} Win, You Won ${standard_payout(hand):,.2f}\n'), PLAYER_WIN
    elif player_hand_value < dealer_hand_value:
        return (f'{msg} Lost\n'), DEALER_WIN

    return '', 0

def clear_and_print(table: Table) -> None:
    """
    Clear the console screen and display the table's current state.

    Args:
        table (Table): The current game table to display.
    """
    clear_terminal()
    print_hands(table)

def print_hands(table: Table) -> None:
    """
    Display the table's current state.

    Args:
        table (Table): The current game table to display.
    """
    buffers = Buffers([], [], [])

    _print_dealer_hands(table, buffers)
    _print_player_hands(table, buffers)

    for strings in buffers.main:
        print(*strings, sep='', end='')

    print()

def _print_dealer_hands(table: Table, buffers: Buffers) -> None:
    """
    Display the dealer's current hand state.

    Depending on the current state of the table, display one or both of the dealer's
    cards, or insurance wager if purchased by the player.

    Args:
        table (Table): The table containing the dealer's hand.
        buffers (Buffers): A named `NamedTuple` containing:
            list: The dealer's string buffer.
            list: the main display string buffer.
    """
    dealer_hand_value = str(get_hand_value(table.dealer))
    dealer_hard_value = str(get_hard_value(table.dealer))

    buffers.dealer.append('Dealer: ')

    # Display only the dealer's first card.
    if table.dealer.is_face_up:
        buffers.dealer.append(
            f'{table.dealer.cards[0].rank_value}\n'
            f'{str(table.dealer.cards[0])}\n'
            '?\n'
        )
    # Display both of the dealer's cards.
    else:
        if is_soft(table.dealer) and not is_twenty_one(table.dealer):
            buffers.dealer.append(f'{dealer_hard_value} / ')

        buffers.dealer.append(f'{dealer_hand_value}\n')

        for card in table.dealer.cards:
            buffers.dealer.append(f'{str(card)}\n')

    if table.player.hands[0].insurance_wager > 0:
        buffers.dealer.append(
            f'Insurance [${table.player.hands[0].insurance_wager:,.2f}]\n'
        )

    buffers.dealer.append('--------------------\n')

    buffers.main.append(buffers.dealer)

def _print_player_hands(table: Table, buffers: Buffers) -> None:
    """
    Display the current state of the player's hand(s).

    Args:
        table (Table): The table containing the player's hand(s).
        buffers (Buffers): A NamedTuple containing:
            - list: The player's string buffer.
            - list: The main display string buffer.
    """
    player_hand_values = [str(get_hand_value(hand)) for hand in table.player.hands]
    player_hard_values = [str(get_hard_value(hand)) for hand in table.player.hands]

    for i, hand in enumerate(table.player.hands):
        buffers.player.append(f'Hand {ROMAN_NUMERALS[i + 1]}: ')

        if is_soft(hand) and not is_twenty_one(hand):
            buffers.player.append(f'{player_hard_values[i]} / ')

        buffers.player.append(
            f'{player_hand_values[i]}'
            f'{_print_wager(table.player.hands[i].wager)}'
        )

        if table.player.hands[i].is_current:
            buffers.player.append(' <- Active\n')
        else:
            buffers.player.append('\n')
        for card in hand.cards:
            buffers.player.append(f'{str(card)}\n')

        buffers.player.append('--------------------\n')

    buffers.player.append(str(table.player.bank))

    buffers.main.append(buffers.player)

def print_initial_outcome(outcome: Outcome, hand: PlayerHand) -> None:
    """
    Display the outcome after the initial deal, if applicable.

    Displays the outcome only if:
        - The player is dealt a blackjack.
        - The dealer is dealt a blackjack.
        - Both the player and dealer are dealt a blackjack (a push).

    Args:
        outcome (Outcome): Contains the outcome flag and payout.
        hand (PlayerHand): The current player hand containing the wager.
    """
    if outcome.flag == PUSH:
        print(f'Round Push, Returned ${hand.wager:,.2f}')
    elif outcome.flag == PLAYER_WIN:
        print(f'Player Blackjack, You Won ${outcome.payout:,.2f}')
    elif outcome.flag == DEALER_WIN:
        print('Dealer Blackjack, You Lose')

def print_initial_insurance_outcome(insurance: Insurance) -> None:
    """
    Display the insurance outcome if purchased by the player.

    Args:
        insurance (Insurance): Contains the insurance activity, win, and payout status.
    """
    if insurance.active and insurance.win:
        print(f'You Won ${insurance.payout:,.2f} With Insurance.')
    elif insurance.active and not insurance.win:
        print('No Dealer Blackjack, Insurance Lost.')

# =======================
# I/O
# Prompt user for input.
# =======================

def _add_chips(table: Table) -> None:
    """
    Prompt the user to add more chips to their bank.
    
    If the user chooses to add more chips, they are continually prompted until
    a valid numeric input within the given bounds is provided. Invalid inputs are 
    caught and handled gracefully. If the user decides not to add more chips,
    exit the program

    Args:
        table (Table): The current game table containing the player whose bank is 
            being updated.
    """
    if request_chips() == YES:
        while True:
            try:
                chips = float(input('Enter the amount of chips to add:\n>'))

                if is_valid_chip_bounds(chips):
                    table.player.bank.chips += chips
                    break

                print(
                    f'Invalid input, please enter a number between '
                    f'{MIN_WAGER:,.2f} and {MAX_WAGER:,.2f}.'
                )

            except ValueError:
                print('Invalid value, `chips` must be a number.')
    else:
        print('\nInsufficient funds to continue playing.')
        # save_chips(table.player.username, table.player.bank.chips, load_user_data())
        sys.exit()

def double_or_not() -> str:
    """
    Prompt the user to decide if they wish to double down.

    The user is continually prompted for an answer until they provide a valid 
    decision. Invalid inputs are caught and handled gracefully.

    Returns:
        str: The user's decision.
    """
    while True:
        choice = input('\nDouble Down? (Y) / (N)\n>')

        if choice.upper() in (YES, NO):
            return choice.upper()

        print('Invalid input, please enter: (Y) YES / (N) NO')

def hit_or_stand() -> str:
    """
    Prompt the user to decide if they wish to hit or stand.

    The user is continually prompted for an answer until they provide a valid 
    decision. Invalid inputs are caught and handled gracefully.

    Returns:
        str: The user's decision.
    """
    while True:
        choice = input('\n(H) HIT / (S) STAND\n>')

        if choice.upper() in (HIT, STAND):
            return choice.upper()
        
        print('Invalid input, please enter: (H) HIT / (S) STAND')

def is_new_round(table: Table) -> bool:
    """
    Prompt the user to decide if they wish to play another round.

    The user is continually prompted for an answer until they provide a valid
    decision. If the answer is no, the current player data is saved onto a local 
    JSON file and the program exits. If the answer is yes, the CLI display is 
    cleared and the function returns `True`.

    Args:
        table (Table): The current game table containing the player data to be saved.
    Returns:
        bool: `True` if the user wishes to continue playing.
    """
    input = request_new_round()

    if input == NO:
        print('\nExiting Blackjack & Saving Data.')
        # save_chips(table.player.username, table.player.bank.chips, load_user_data())
        sys.exit()
    elif input == YES:
        clear_terminal()
        return True

    return False

def wager_prompt(table: Table) -> float:
    """
    Prompt the user for a valid wager amount.

    If the player's bank balance is less than the `MIN_WAGER`, prompt them to add
    more chips. The user is then continually prompted until they enter:
        - A valid numeric input.
        - An amount between `MIN_WAGER` and `MAX_WAGER`.
        - An amount that does not exceed their current bank balance

    Args:
        table (Table): The current game table containing the player placing the wager.

    Returns:
        float: The validated wager amount.
    """
    print(_print_min_wager(table.player.bank))

    while True:
        try:
            if not is_valid_wager(table.player.bank.chips):
                # Prompt the user to add more chips
                _wager_prompt_helper(table) 

            wager = float(input('Enter Wager:\n>'))

            valid_wager = is_valid_player_wager(table.player, wager)
            valid_wager_bounds = is_valid_chip_bounds(wager)

            if valid_wager and valid_wager_bounds:
                return wager
            elif not valid_wager:
                _wager_prompt_helper(table)
            elif not valid_wager_bounds:
                print(
                    f'Invalid wager, please enter a number between '
                    f'{MIN_WAGER:,.2f} and {MAX_WAGER:,.2f}'
                )

        except ValueError:
            print('Invalid value, please enter a valid number.')

def _wager_prompt_helper(table: Table) -> None:
    """
    Prompt the user to add chips if their balance is below the minimum wager.

    Args:
        table (Table): The game table containing the player placing the wager.
    """
    print('Not enough chips.')

    _add_chips(table)

    clear_terminal()
    print(_print_min_wager(table.player.bank))

def request_chips() -> str:
    """
    Prompt the user if they wish to add chips.

    The user is continually prompted for an answer until they provide a valid 
    decision. Invalid inputs are caught and handled gracefully.

    Returns:
        str: The user's decision.
    """
    while True:
        choice = input('Add chips? (Y) / (N)\n>')
        
        if choice.upper() in (YES, NO):
            return choice.upper()
        
        print('Invalid input, please enter: (Y) YES / (N) NO')

def request_insurance(cost: float) -> str:
    """
    Prompt the user if they wish to purchase insurance.

    The user is continually prompted for an answer until they provide a valid 
    decision. Invalid inputs are caught and handled gracefully.

    Args:
        cost (float): The current cost for purchasing insurance.

    Returns:
        str: The user's decision.
    """
    while True:
        choice = input(f'\nInsurance? ${cost:,.2f} (Y) / (N)\n>')
        
        if choice.upper() in (YES, NO):
            return choice.upper()
        
        print('Invalid input, please enter: (Y) YES / (N) NO')

def request_new_round() -> str:
    """
    Prompt the user if they wish to start a new round.

    The user is continually prompted for an answer until they provide a valid 
    decision. Invalid inputs are caught and handled gracefully.

    Returns:
        str: The user's decision.
    """
    while True:
        choice = input('\nContinue? (Y) / (N)\n>')
        
        if choice.upper() in (YES, NO):
            return choice.upper()
        
        print('Invalid input, please enter: (Y) YES / (N) NO')

def split_or_not() -> str:
    """
    Prompt the user if they wish to split.

    The user is continually prompted for an answer until they provide a valid 
    decision. Invalid inputs are caught and handled gracefully.

    Returns:
        str: The user's decision.
    """
    while True:
        choice = input('\nSplit? (Y) / (N)\n>')
        
        if choice.upper() in (YES, NO):
            return choice.upper()
        
        print('Invalid input, please enter: (Y) YES / (N) NO')
  
# ================
# DISPLAY HELPERS
# ================

def _print_min_wager(bank: Bank) -> str:
    """
    Return a formatted string of the player's bank balance and the `MIN_WAGER`.

    Args:
        bank (Bank): The player's bank containing the current balance.
    
    Returns:
        str: The string representation of the player's balance and the 
            table's `MIN_WAGER`.
    """
    return (
        f'{str(bank)}\n'
        f'Minimum Wager is: $' + f'{MIN_WAGER:,.2f}\n'
    )

def clear_terminal() -> None:
    """Clear the CLI display."""
    subprocess.run('cls', shell=True)

def get_round_outcome_msg(index: int, flag: str) -> str:
    """
    Return a formatted string of the player's end of round state based on the 
    provided flag.

    Args:
        index (int): The index of the player's current hand.
        flag (str): The flag containing the game round state.

    Returns:
        str: The formatted outcome message.
    """
    if flag == BUST:
        return f'Hand {ROMAN_NUMERALS[index + 1]} Busted & Lost\n'
    elif flag == PLAYER_WIN:
        return f'Hand {ROMAN_NUMERALS[index + 1]} Win. '
    return ''

def get_round_outcome_payout_msg(hand: PlayerHand) -> str:
    """ 
    Return a formatted string for a standard blackjack win based off of the player's
    current wager.

    Args:
        hand (PlayerHand): The hand containing the placed wager.

    Returns:
        str: The formatted payout message.
    """
    return f'You Won ${standard_payout(hand):,.2f}\n'

def load_timer(key: int = -1) -> None:
    """
    Display a live countdown timer in the CLI.

    Fetches a timer message using the provided key and updates the console, counting
    down from 3 to 1.

    Args:
        key (int, optional): The dictionary key for the timer message. 
            Defaults to `-1`.
    """
    msg = TIMER_MESSAGES.get(key, '{}')

    print()

    for i in range(3, 0, -1):
        print(msg.format(i), end='\r')
        time.sleep(1)
  
def print_dealer_state(flag: str) -> None:
    """
    Display the dealer's state at the end of the round using the provided flag.

    Args:
        flag (str): The flag containing the game round state.
    """
    if flag == STAND:
        print('Dealer is Standing')
    elif flag == BUST:
        print('Dealer has Busted')

def print_stand_or_bust(index: int, flag: str) -> None:
    """
    Display the current hand status based on the provided flag.

    Args:
        index (int): The index of the current hand.
        flag (str): The flag containing the hand status.
    """
    if flag == STAND:
        print(f'Hand {ROMAN_NUMERALS[index + 1]} is Standing')
    elif flag == BUST:
        print(f'Hand {ROMAN_NUMERALS[index + 1]} has Busted')

def _print_wager(wager: float) -> str:
    """
    Return a formatted string for the player's current wager.

    Args:
        wager (float): The player's current placed wager.

    Returns:
        str: The formatted string.
    """
    return f' [${wager:,.2f}]'
