"""
Tests for the `interface.py` module.

Contains tests for validating game state displays, including:
- Displaying current table state.
- Prompting user for input.
- Formatting display messages. 
"""

__author__ = 'Adrien P.'

import pytest
import time

from bank import Bank
from card import Card
import constants
from datatypes import (
    DealerHand,
    Insurance,
    Outcome,
    Player,
    PlayerHand,
    Table,
)
import interface

def _generate_basic_input_arg_params(choice):
    """
    Provide a list of functions with the following:
    - Test arguments (all but one are None).
    - List of mock inputs to use when the function is called.
    """
    return [
        (interface.double_or_not, [], choice),
        (interface.request_chips, [], choice),
        (interface.request_insurance, [7.5], choice),
        (interface.request_new_round, [], choice),
        (interface.split_or_not, [], choice),
    ]

@pytest.mark.parametrize(
    'function, args, expected_choice',
    [
        *_generate_basic_input_arg_params(constants.YES)
    ],
)
def test_yes_flow(mock_inputs, capsys, function, args, expected_choice):
    mock_inputs(['yes', '0', 'sadf', 'y'])

    choice = function(*args)

    result = capsys.readouterr()

    assert result.out.count('Invalid input, please enter: (Y) YES / (N) NO\n') == 3
    assert choice == expected_choice

@pytest.mark.parametrize(
    'function, args, expected_choice',
    [
        *_generate_basic_input_arg_params(constants.NO)
    ],
)
def test_no_flow(mock_inputs, capsys, function, args, expected_choice):
    mock_inputs(['no', '0', 'sadf', 'n'])

    choice = function(*args)

    result = capsys.readouterr()

    assert result.out.count('Invalid input, please enter: (Y) YES / (N) NO\n') == 3
    assert choice == expected_choice

@pytest.mark.parametrize(
    'player_cards, test_wager, index, dealer_cards, expected_msg, expected_flag',
    [
        (
            [Card('Spades', 5), Card('Clubs', 5)], 
            15.0,
            0,
            [Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)],
            'Hand I Lost\n',
            constants.DEALER_WIN,
        ),
        (
            [Card('Spades', 5), Card('Clubs', 5), Card('Hearts', 7)], 
            15.0,
            1,
            [Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)],
            'Hand II Push, Returned $15.00\n',
            constants.PUSH,
        ),
        (
            [Card('Spades', 5), Card('Clubs', 5), Card('Hearts', 8)], 
            15.0,
            1,
            [Card('Diamonds', 4), Card('Hearts', 6), Card('Spades', 7)],
            'Hand II Win, You Won $30.00\n',
            constants.PLAYER_WIN,
        ),
    ],
    ids=[
        'dealer_win_output',
        'push_output',
        'player_win_output',
    ],
)
def test_compare_hands_output(
        player_cards,
        test_wager,
        index,
        dealer_cards,
        expected_msg,
        expected_flag,
):
    if index == 0:
        player_hand1 = PlayerHand(cards=player_cards, wager=test_wager)
        player_hand2 = PlayerHand(cards=[], wager=0.0)
    elif index == 1:
        player_hand1 = PlayerHand(cards=[], wager=0.0)
        player_hand2 = PlayerHand(cards=player_cards, wager=test_wager)

    table = Table(
        player=Player(username='Test', hands=[player_hand1, player_hand2]),
        dealer=DealerHand(cards=dealer_cards)
    )

    msg, flag = interface.compare_hands(table, table.player.hands[index], index)

    assert msg == expected_msg
    assert flag == expected_flag

@pytest.fixture
def base_table():
    """
    Provide a `Table` instance with one hand for the `Player` and one hand for 
    the dealer.
    """
    return Table (
        player=Player(
            username='Test',
            hands=[
                PlayerHand(cards=[Card('Spades', 4), Card('Hearts', 6)], wager=15.0)
            ],
        ),
        dealer=DealerHand(cards=[Card('Clubs', 'Ace'), Card('Diamonds', 3)]),
    )

def test_print_player_hands_init_deal_no_insurance(capsys, base_table):
    base_table.player.bank = Bank(30.0)

    interface.clear_and_print(base_table)

    result = capsys.readouterr()

    assert result.out == (
        'Dealer: 11\n'
        '♣Ace\n'
        '?\n'
        '--------------------\n'
        'Hand I: 10 [$15.00]\n'
        '♠4\n'
        '♥6\n'
        '--------------------\n'
        'Chips: $30.00\n'
    )

def test_print_player_hands_init_deal_with_insurance(capsys, base_table):
    base_table.player.bank = Bank(22.5)
    base_table.player.hands[0].insurance_wager = 7.5

    interface.clear_and_print(base_table)

    result = capsys.readouterr() 

    assert result.out == (
        'Dealer: 11\n'
        '♣Ace\n'
        '?\n'
        'Insurance [$7.50]\n'
        '--------------------\n'
        'Hand I: 10 [$15.00]\n'
        '♠4\n'
        '♥6\n'
        '--------------------\n'
        'Chips: $22.50\n'
    )

@pytest.fixture
def split_hand_table():
    """
    Provide a `Table` instance with split hands for the `Player` and no cards
    for the dealer.
    """
    return Table(
        player=Player(
            username='Test',
            bank=Bank(50.0),
            hands=[
                PlayerHand(
                    cards=[Card('Clubs', 4), Card('Spades', 6), Card('Hearts', 6)],
                    wager=30.0,
                 ),
                PlayerHand(
                    cards=[Card('Hearts', 'Jack'), Card('Spades', 4)],
                    wager=30.0,
                 ),
            ],
        ),
        dealer=(DealerHand(is_hidden=False)),
    )

def test_print_player_hands_dealer_showing_both_cards_soft(capsys, split_hand_table):
    split_hand_table.player.hands[0].is_active = True
    split_hand_table.dealer.cards = [Card('Spades', 'Ace'), Card('Hearts', 4)]

    interface.print_hands(split_hand_table)

    result = capsys.readouterr() 

    assert result.out == (
        'Dealer: 5 / 15\n'
        '♠Ace\n'
        '♥4\n'
        '--------------------\n'
        'Hand I: 16 [$30.00] <- Active\n'
        '♣4\n'
        '♠6\n'
        '♥6\n'
        '--------------------\n'
        'Hand II: 14 [$30.00]\n'
        '♥Jack\n'
        '♠4\n'
        '--------------------\n'
        'Chips: $50.00\n'
    )

def test_print_player_hands_dealer_showing_both_cards_non_soft(
    capsys,
    split_hand_table,
):
    split_hand_table.player.hands[1].is_active = True
    split_hand_table.dealer.cards = [Card('Spades', 8), Card('Hearts', 4)]

    interface.print_hands(split_hand_table)

    result = capsys.readouterr() 

    assert result.out == (
        'Dealer: 12\n'
        '♠8\n'
        '♥4\n'
        '--------------------\n'
        'Hand I: 16 [$30.00]\n'
        '♣4\n'
        '♠6\n'
        '♥6\n'
        '--------------------\n'
        'Hand II: 14 [$30.00] <- Active\n'
        '♥Jack\n'
        '♠4\n'
        '--------------------\n'
        'Chips: $50.00\n'
    )

@pytest.mark.parametrize(
    'test_wager, flag, expected_display, expected_payout',
    [
        (15.0, constants.PUSH, 'Round Push, Returned $15.00\n', 0.0),
        (15.0, constants.PLAYER_WIN, 'Player Blackjack, You Won $37.50\n', 37.5),
        (15.0, constants.DEALER_WIN, 'Dealer Blackjack, You Lose\n', 0.0),
        (15.0, 0, '', 0.0),
    ],
    ids=[
        'initial_push_outcome',
        'initial_player_blackjack_outcome',
        'initial_dealer_blackjack_outcome',
        'initial_no_outcome',
    ],
)
def test_initial_outcome_display(
    capsys,
    test_wager,
    flag,
    expected_display,
    expected_payout,
):
    hand = PlayerHand(wager=test_wager)
    outcome = Outcome(flag=flag, payout=expected_payout)

    interface.print_initial_outcome(outcome, hand)

    result = capsys.readouterr()

    assert result.out == expected_display

@pytest.mark.parametrize(
    'test_active, test_win, test_payout, expected_display',
    [
        (True, True, 15.0, 'You Won $15.00 With Insurance.\n'),
        (True, False, 0.0, 'No Dealer Blackjack, Insurance Lost.\n'),
        (False, False, 0.0, ''),
    ],
    ids=[
        'insurance_win',
        'insurance_lost',
        'no_insurance',
    ],
)
def test_initial_insurance_outcome_display(
    capsys,
    test_active,
    test_win,
    test_payout,
    expected_display,
):
    insurance = Insurance(active=test_active, win=test_win, payout=test_payout)

    interface.print_initial_insurance_outcome(insurance)

    result = capsys.readouterr()

    assert result.out == expected_display

def test_hit_hand_decision(mock_inputs, capsys):
    mock_inputs(['hit', 'n', '4', 'h'])

    choice = interface.hit_or_stand()

    result = capsys.readouterr()

    assert 'Invalid input, please enter: (H) HIT / (S) STAND\n' in result.out
    assert result.out.count('Invalid input, please enter: (H) HIT / (S) STAND\n') == 3

    assert choice == 'H'

def test_stand_hand_decision(mock_inputs, capsys):
    mock_inputs(['t', 'g', 'sadfa', 'stand', 's'])

    choice = interface.hit_or_stand()

    output = capsys.readouterr()

    assert 'Invalid input, please enter: (H) HIT / (S) STAND\n' in output.out
    assert output.out.count('Invalid input, please enter: (H) HIT / (S) STAND\n') == 4

    assert choice == 'S'

def test_add_chips_to_player_bank(mock_inputs, base_table):
    mock_inputs(['y', '10', '35'])

    base_table.player.bank = Bank(10.0)

    interface._add_chips(base_table)

    assert base_table.player.bank.chips == 45.0

def test_add_chips_deny_and_program_exit(mock_inputs, base_table):
    mock_inputs(['n', '10', '35'])

    with pytest.raises(SystemExit) as exe_info:
        interface._add_chips(base_table)

    assert exe_info.value.code == None

def test_is_new_round_continue(mock_inputs):
    table = Table(Player(username='Test'))

    mock_inputs(['y'])

    assert interface.is_new_round(table) == True

def test_is_new_round_exit_branch(mock_inputs, monkeypatch):
    table = Table(Player(username='Test'))

    mock_inputs(['n'])

    # monkeypatch.setattr(interface, 'save_chips', lambda *args, **kwargs: None)

    with pytest.raises(SystemExit) as exe_info:
        interface.is_new_round(table)

    assert exe_info.value.code is None

@pytest.mark.parametrize(
    'chips, input, expected_wager',
    [
        (25, ['15'], 15.0),
        (1.0, ['15', '20', 'y', '20', '15'], 15.0),
        (15.0, ['asdf', '15'], 15.0),
    ],
    ids=[
        'wager_prompt_has_enough_chips',
        'wager_prompt_player_bank_is_broke',
        'wager_invalid_input_caught_gracefully',
    ]
)
def test_wager_prompt(mock_inputs, chips, input, expected_wager, base_table):
    base_table.player.bank = Bank(chips)

    mock_inputs(input)

    assert interface.wager_prompt(base_table) == expected_wager

def test_wager_prompt_deny_adding_chips(mock_inputs, base_table):
    mock_inputs(['14', 'n'])

    base_table.player.bank = Bank(30.0)

    with pytest.raises(SystemExit) as exe_info:
        interface.wager_prompt(base_table)

    assert exe_info.value.code is None

@pytest.mark.parametrize(
    'key, expected_output',
    [
        (1, 'Dealer is peeking...'),
        (2, 'Switching active hand...'),
        (3, 'Switching to dealer...'),
        (4, 'Dealer is hitting...'),
        (5, 'Comparing hand values...'),
        (6, 'Dealer is flipping card...'),
        (7, 'You cannot afford that...'),
        (-1, ''),
        (999, ''),
    ]
)
def test_load_timer(capsys, monkeypatch, key, expected_output):
    monkeypatch.setattr(time, 'sleep', lambda x: None)

    interface.load_timer(key)

    output = capsys.readouterr()

    assert expected_output in output.out

@pytest.mark.parametrize(
    'flag, expected_display',
    [
        (constants.STAND, 'Dealer is Standing\n'),
        (constants.BUST, 'Dealer has Busted\n'),
    ]
)
def test_display_dealer_state(capsys, flag, expected_display):
    interface.print_dealer_state(flag)

    output = capsys.readouterr()

    assert expected_display in output.out

@pytest.mark.parametrize(
    'flag, index, expected_display',
    [
        (constants.BUST, 0, 'Hand I Busted & Lost\n'),
        (constants.BUST, 1, 'Hand II Busted & Lost\n'),
        (constants.PLAYER_WIN, 0, 'Hand I Win. '),
        (constants.PLAYER_WIN, 1, 'Hand II Win. '),
    ]
)
def test_get_round_outcome_msg(flag, index, expected_display):
    assert interface.get_round_outcome_msg(index, flag) == expected_display

@pytest.mark.parametrize(
    'flag, index, expected_display',
    [
        (constants.STAND, 0, 'Hand I is Standing\n'),
        (constants.STAND, 1, 'Hand II is Standing\n'),
        (constants.BUST, 0, 'Hand I has Busted\n'),
        (constants.BUST, 1, 'Hand II has Busted\n')
    ]
)
def test_print_stand_or_bust(capsys, index, flag, expected_display):
    interface.print_stand_or_bust(index, flag)

    console = capsys.readouterr()

    assert expected_display in console.out
