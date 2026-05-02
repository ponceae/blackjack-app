""" 
This module tests the `game.py` module.

Validates and ensures correct game loop execution and logic.
"""

__author__ = 'Adrien P.'

import pytest
import time

from actions import create_and_shuffle
from bank import Bank
from card import Card
import constants
from datatypes import (
    DealerHand,
    Insurance,
    Outcome,
    PlayerAction,
    Player,
    PlayerHand,
    SplitHands,
    Table,
)
import game

@pytest.fixture(autouse=True)
def suppress_ui_and_timer(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda x: None)
    monkeypatch.setattr(
        'interface.clear_and_print', 
        lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        'conditions.compare_initial_hands', 
        lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        'interface.print_initial_insurance_outcome', 
        lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        'interface.print_hands',
        lambda *args, **kwargs: None
    )

# ==================================================
# INITIAL ROUND TESTS
# ==================================================

@pytest.fixture
def init_table():
    return Table(
        player=Player(
            username='Test',
            bank=Bank(25.0),
            hands=[
                PlayerHand(
                    cards=[Card('Hearts', 6), Card('Clubs', 4)],
                    wager= 15.0,
                ), 
            ],
        ),
        dealer=DealerHand(cards=[Card('Diamonds', 'Ace'), Card('Spades', 5)]),
    )

@pytest.mark.parametrize(
    'insurance, inputs, chips, active_test, expected_cost, expected_chips',
    [
        (Insurance(), ['y'], 25.0, True, 7.5, 17.5),
        (Insurance(), ['n'], 5.0, False, 0.0, 5.0),
        (Insurance(), ['n'], 25.0, False, 0.0, 25.0),
    ],
    ids=[
        'insurance_purchased',
        'invalid_bank',
        'insurance_denied',
    ],
)
def test_handle_insurance_on_init_deal_not_broke_bank(
    mock_inputs, 
    init_table,
    insurance,
    inputs,
    chips,
    active_test,
    expected_cost,
    expected_chips,
):
    init_table.player.bank = Bank(chips)
    
    mock_inputs(inputs)

    game._handle_insurance(insurance, init_table)

    assert insurance.active == active_test

    assert init_table.player.hands[0].insurance_wager == expected_cost
    assert init_table.player.bank.chips == expected_chips

def test_insurance_helper_on_init_deal(
    mock_inputs,
    init_table
):
    insurance = Insurance(active=True)

    mock_inputs(['y'])

    game._handle_insurance(insurance, init_table)
    game._insurance_helper(insurance, init_table)

    assert init_table.player.bank.chips == 32.5

@pytest.mark.parametrize(
    'outcome_flag, expected_payout, expected_chips',
    [
        (constants.DEALER_WIN, 0.0, 25.0),
        (constants.PUSH, 15.0, 40.0),
        (constants.PLAYER_WIN, 37.5, 62.5),
    ],
)
def test_handle_outcomes_on_init_deal(
    monkeypatch,
    init_table,
    outcome_flag,
    expected_payout,
    expected_chips,
):
    outcome = Outcome(flag=outcome_flag)

    monkeypatch.setattr(game, '_insurance_helper', lambda *args, **kwargs: None)

    game._handle_outcomes(outcome, Insurance(), init_table)

    assert outcome.payout == expected_payout

    assert init_table.player.bank.chips == expected_chips

def test_exe_init_no_winners_no_insurance_purchased(monkeypatch, init_table):
    monkeypatch.setattr(game, '_handle_insurance', lambda *args, **kwargs: None)	

    assert game.exe_initial_cond(init_table) == False

def test_exe_init_no_winners_no_insurance_win(monkeypatch, init_table):
    init_table.player.hands[0].insurance_wager = 7.5

    def fake_handle_insurance(insurance, table):
        insurance.active = True

    monkeypatch.setattr(game, '_handle_insurance', fake_handle_insurance)

    assert game.exe_initial_cond(init_table) == False

    assert init_table.player.hands[0].insurance_wager == 0

# def test_exe_init_round_ending_cond_no_new_round(mock_inputs, monkeypatch, init_table):
#     mock_inputs(['n'])

#     monkeypatch.setattr(
#         'conditions.compare_initial_hands', 
#         lambda _: constants.PLAYER_WIN
#     )

#     monkeypatch.setattr(game, '_handle_insurance', lambda *args, **kwargs: None)
#     monkeypatch.setattr(game, '_handle_outcomes', lambda *args, **kwargs: None)

#     monkeypatch.setattr(
#         "interface.request_new_round",
#         lambda: constants.NO
#     )

#     monkeypatch.setattr('interface.save_chips', lambda *args, **kwargs: None)

#     with pytest.raises(SystemExit) as exe_info:
#         game.exe_initial_cond(init_table)

#     assert exe_info.value.code == None

# def test_exe_init_round_ending_cond_with_new_round(monkeypatch, init_table):
#     monkeypatch.setattr(
#         'conditions.compare_initial_hands', 
#         lambda _: constants.PLAYER_WIN
#     )
#     monkeypatch.setattr(game, '_handle_insurance', lambda *args, **kwargs: None)
#     monkeypatch.setattr(game, '_handle_outcomes', lambda *args, **kwargs: None)

#     monkeypatch.setattr(
#         "interface.request_new_round",
#         lambda: constants.YES
#     )

#     monkeypatch.setattr('interface.save_chips', lambda *args, **kwargs: None)

#     assert game.exe_initial_cond(init_table) == True

# ==================================================
# PLAYER TURN TESTS
# ==================================================

@pytest.fixture
def full_table():
    return Table(
        player=Player(
            username='Test',
            bank=Bank(25.0),
            hands=[
                PlayerHand(
                    cards=[Card('Hearts', 5), Card('Clubs', 5)],
                    wager= 15.0,
                ), 
            ],
        ),
        dealer=DealerHand(cards=[Card('Diamonds', 4), Card('Spades', 5)]),
        deck=create_and_shuffle()
    )

@pytest.mark.parametrize(
    'cards, expected_chips, str_a, str_b, split_ace',
    [
        ([Card('Hearts', 5), Card('Clubs', 5)], 10.0, '♥5', '♣5', False),
        ([Card('Hearts', 'Ace'), Card('Clubs', 'Ace')], 10.0, '♥Ace', '♣Ace', True)
    ],
)
def test_handle_split_hands_normal_path(
    mock_inputs,
    full_table,
    cards,
    expected_chips,
    str_a,
    str_b,
    split_ace,
):
    mock_inputs(['y'])

    split_status = SplitHands()

    full_table.player.hands[0].cards = cards

    game._handle_split(full_table, split_status)

    assert full_table.player.bank.chips == expected_chips

    assert full_table.player.hands[0].cards[0].to_string() == str_a
    assert full_table.player.hands[1].cards[0].to_string() == str_b

    assert full_table.player.hands[1].wager == full_table.player.hands[0].wager

    assert split_status.split_hand == True
    assert split_status.split_aces == split_ace

@pytest.mark.parametrize(
    'input, chips',
    [
        (['n'], 25.0),
        (['y'], 10.0),
    ],
    ids=[
        'split_hand_deny',
        'cannot_afford_split',
    ],
)
def test_handle_split_hands_unhappy_path(
    monkeypatch,
    mock_inputs,
    full_table,
    input,
    chips
):
    split_status = SplitHands()

    full_table.player.bank = Bank(chips)

    mock_inputs(input)

    monkeypatch.setattr(time, 'sleep', lambda x: None)

    game._handle_split(full_table, split_status)

    assert full_table.player.bank.chips == chips

    assert full_table.player.hands[0].cards[0].to_string() == '♥5'
    assert full_table.player.hands[0].cards[1].to_string() == '♣5'

    assert len(full_table.player.hands) == 1

    assert split_status.split_hand == False

@pytest.mark.parametrize(
    'is_split, index, hands, expected_bool',
    [
        (
            True,
            0,
            [
                [Card('Clubs', 4), Card('Hearts', 5)], 
                [],
            ],
            True,
        ),
        (
            False,
            0, 
            [
                [Card('Clubs', 4), Card('Hearts', 5)],
                [Card('Spades', 6), Card('Clubs', 7)],
            ],
            False
        ),
        (
            True,
            1,
            [
                [], 
                [Card('Spades', 6), Card('Clubs', 7)],
            ],
            False
        ),
    ],
    ids=[
        'split_hands_hand_left',
        'non_split_hand_no_more_hands',
        'split_hand_no_hands_left'
    ],
)
def test_hand_left_in_hands(monkeypatch, is_split, index, hands, expected_bool):
    hands = hands

    split_status = SplitHands(split_hand=is_split)

    monkeypatch.setattr(time, 'sleep', lambda x: None)

    assert game._hands_left(split_status, hands, index) == expected_bool

@pytest.mark.parametrize(
    'is_split, player_hands, index, expected_action',
    [
        (
            True,
            [
                PlayerHand(cards=[]), 
                PlayerHand(cards=[Card('Clubs', 4), Card('Hearts', 5)], wager=15.0),
            ],
            1,
            PlayerAction.END_TURN,
        ),
        (
            True,
            [
                PlayerHand(cards=[Card('Clubs', 5), Card('Hearts', 6)], wager=15.0), 
                PlayerHand(cards=[]),
            ],
            0,
            PlayerAction.NEXT_HAND,	
        ),
        (
            False,
            [
                PlayerHand(cards=[Card('Clubs', 5), Card('Hearts', 6)], wager=15.0), 
                PlayerHand(cards=[]),
            ],
            0,
            PlayerAction.END_TURN,	
        ),
    ],
    ids=[
        'split_hand_double_down_no_hands_left',
        'split_hand_double_down_hand_left',
        'non_split_hand_double_down',
    ],
)
def test_handle_double_down_affordability(
    monkeypatch,
    full_table,
    is_split,
    player_hands,
    index,
    expected_action
):
    full_table.player.hands = player_hands

    split_status = SplitHands(split_hand=is_split)

    monkeypatch.setattr(time, 'sleep', lambda x: None)

    action = game._handle_double_down(full_table, index, split_status)

    assert full_table.player.hands[index].wager == 30.0
    assert full_table.player.bank.chips == 10.0

    assert action == expected_action

    assert len(full_table.player.hands[index].cards) == 3

@pytest.mark.parametrize(
    'inputs, is_split, player_hands, index, card, expected_action',
    [
        (
            ['h', 's'], 
            True, 
            [
                PlayerHand(cards=[Card('Spades', 6), Card('Hearts', 4)]),
                PlayerHand(cards=[]),
            ],
            0,
            Card('Hearts', 8),
            PlayerAction.NEXT_HAND
        ),
        (
            ['h'],
            True,
            [
                PlayerHand(cards=[]),
                PlayerHand(cards=[Card('Spades', 10), Card('Hearts', 5)]),
            ],
            1,
            Card('Hearts', 9),
            PlayerAction.END_TURN,
        ),
        (
            ['h'],
            True,
            [
                PlayerHand(cards=[Card('Spades', 10), Card('Hearts', 5)]),
                PlayerHand(cards=[]),
            ],
            0,
            Card('Hearts', 9),
            PlayerAction.NEXT_HAND,
        ),
        (
            ['h'],
            True,
            [
                PlayerHand(cards=[Card('Spades', 10), Card('Hearts', 5)]),
                PlayerHand(cards=[]),
            ],
            0,
            Card('Hearts', 6),
            PlayerAction.NEXT_HAND,
        ),
        (
            ['h'],
            False,
            [
                PlayerHand(cards=[Card('Spades', 10), Card('Hearts', 5)]),
                PlayerHand(cards=[]),
            ],
            0,
            Card('Hearts', 6),
            PlayerAction.END_TURN,
        ),
    ],
    ids=[
        'hit_once_then_stand_on_split_hand',
        'hit_once_and_bust_on_non_split',
        'hit_once_and_bust_on_split_hand_left',
        'hit_once_and_stand_on_split_hand_left',
        'hit_once_and_stand_on_non_split_no_hand_left',
    ],
)
def test_handle_hitting(
    monkeypatch,
    mock_inputs,
    full_table,
    inputs,
    is_split,
    player_hands,
    index,
    card,
    expected_action
):
    full_table.player.hands = player_hands

    split_status = SplitHands(split_hand=is_split)

    mock_inputs(inputs)

    def fake_handle_hitting(*args, **kwargs):
        full_table.player.hands[index].cards.append(card)

    monkeypatch.setattr(time, 'sleep', lambda x: None)
    monkeypatch.setattr('actions.hit_hand', fake_handle_hitting)

    action = game._handle_hitting(
        full_table,
        split_status,
        full_table.player.hands[index],
        index,
    )

    assert action == expected_action

def test_exe_player_control_split_aces_early_exit(monkeypatch, full_table):
    called_split = []
    def fake_handle_split(_, split):
        split.split_aces = True
        called_split.append(True)

    monkeypatch.setattr(game, '_handle_split', fake_handle_split)

    game.exe_player_control(full_table)

    assert called_split

def test_exe_player_control_double_down_no_hands_left(monkeypatch, full_table):
    monkeypatch.setattr(game, '_handle_split', lambda *args, **kwargs: None)

    monkeypatch.setattr('interface.double_or_not', lambda: constants.YES)
    monkeypatch.setattr(
        'conditions.is_valid_doubled_wager', 
        lambda *args, **kwargs: True
    )

    monkeypatch.setattr(
        game, 
        '_handle_double_down', 
        lambda *args, **kwargs: PlayerAction.END_TURN
    )

    game.exe_player_control(full_table)

    assert full_table.player.hands[0].is_active == False

def test_exe_player_control_double_down_hands_left(monkeypatch, full_table):
    full_table.player.hands.append(
            PlayerHand(cards=[Card('Hearts', 3), Card('Spades', 4)])
        )

    monkeypatch.setattr(game, '_handle_split', lambda *args, **kwargs: None)

    monkeypatch.setattr('interface.double_or_not', lambda: constants.YES)
    monkeypatch.setattr(
        'conditions.is_valid_doubled_wager', 
        lambda *args, **kwargs: True
    )

    actions = iter([
        PlayerAction.NEXT_HAND,
        PlayerAction.END_TURN
    ])

    monkeypatch.setattr(
        game, 
        '_handle_double_down', 
        lambda *args, **kwargs: next(actions)
    )

    game.exe_player_control(full_table)

    assert all(not hand.is_active for hand in full_table.player.hands)

def exe_player_control_next_hand(monkeypatch, full_table):
    full_table.player.hands.append(
        PlayerHand(cards=[Card('Hearts', 3), Card('Spades', 4)])
    )

    def fake_handle_split(table, split):
        split.split_hand = True

    monkeypatch.setattr('interface.handle_split', fake_handle_split)

    monkeypatch.setattr('interface.double_or_not', lambda: constants.NO)

    handle_hitting_calls = []
    def fake_handle_hitting(*_, i):
        handle_hitting_calls.append(i)
        return PlayerAction.NEXT_HAND

    monkeypatch.setattr(game, '_handle_hitting', fake_handle_hitting)

    game.exe_player_control(full_table)

    assert 0 in handle_hitting_calls
    assert 1 in handle_hitting_calls

def exe_player_control_end_turn(monkeypatch, full_table):
    monkeypatch.setattr(
        'interface.handle_split', 
        lambda *args, **kwargs: None
    )

    monkeypatch.setattr('interface.double_or_not', lambda: constants.NO)

    handle_hitting_calls = []
    def fake_handle_hitting(*_, i):
        handle_hitting_calls.append(i)
        return PlayerAction.END_TURN
    
    monkeypatch.setattr(game, '_handle_hitting', fake_handle_hitting)

    game.exe_player_control(full_table)

    assert handle_hitting_calls == [0]

# ======================
# DEALER TURN TESTS.
# ======================

def test_exe_dealer_control_is_bust(monkeypatch, full_table):
    monkeypatch.setattr('actions.get_hand_value', lambda _: 16)
    
    monkeypatch.setattr('actions.hit_hand', lambda *args, **kwargs: None)

    monkeypatch.setattr('conditions.is_bust', lambda _: True)

    monkeypatch.setattr(
        'interface.print_dealer_state', 
        lambda *args, **kwargs: None
    )

    assert game.exe_dealer_control(full_table) == None

def test_exe_dealer_control_is_twenty_one(monkeypatch, full_table):
    monkeypatch.setattr('actions.get_hand_value', lambda _: 16)
    
    monkeypatch.setattr('actions.hit_hand', lambda *args, **kwargs: None)

    monkeypatch.setattr('conditions.is_twenty_one', lambda _: True)

    monkeypatch.setattr(
        'interface.print_dealer_state', 
        lambda *args, **kwargs: None
    )

    assert game.exe_dealer_control(full_table) == None

def test_exe_dealer_control_two_card_stand(monkeypatch, full_table):
    monkeypatch.setattr('actions.get_hand_value', lambda _: 17)
    
    monkeypatch.setattr(
        'interface.print_dealer_state', 
        lambda *args, **kwargs: None
    )

    assert game.exe_dealer_control(full_table) == None

def test_exe_dealer_control_stand_after_hit(monkeypatch, full_table):
    values = iter([
        14, 19
    ])
    
    monkeypatch.setattr('actions.get_hand_value', lambda _: next(values))

    monkeypatch.setattr('actions.hit_hand', lambda *args, **kwargs: None)

    monkeypatch.setattr(
        'interface.print_dealer_state', 
        lambda *args, **kwargs: None
    )

    assert game.exe_dealer_control(full_table) == None

# =======================
# ROUND END CHECK TESTS.
# =======================

def test_verify_round_end_cond_player_bust(monkeypatch, full_table):
    def fake_is_bust(hand):
        if isinstance(hand, PlayerHand):
            return True

    monkeypatch.setattr('conditions.is_bust', fake_is_bust)

    round_outcome_calls = []
    def spy_get_round_outcome_msg(i, flag):
        round_outcome_calls.append((i, flag))
        return 'PLAYER BUST'

    monkeypatch.setattr(
        'interface.get_round_outcome_msg', 
        spy_get_round_outcome_msg
    )

    monkeypatch.setattr(
        'interface.is_new_round', 
        lambda *args, **kwargs: None
    )

    game.verify_round_end_cond(full_table)

    assert round_outcome_calls[0] == (0, constants.BUST)
    assert len(round_outcome_calls) == 1

def test_verify_round_end_cond_dealer_bust(monkeypatch, full_table):
    def fake_is_bust(hand):
        if isinstance(hand, DealerHand):
            return True

    monkeypatch.setattr('conditions.is_bust', fake_is_bust)

    round_outcome_calls = []
    def spy_get_round_outcome_msg(i, flag):
        round_outcome_calls.append((i, flag))
        return 'DEALER BUST'

    monkeypatch.setattr(
        'interface.get_round_outcome_msg', 
        spy_get_round_outcome_msg
    )

    monkeypatch.setattr(
        'interface.is_new_round', 
        lambda *args, **kwargs: None
    )

    game.verify_round_end_cond(full_table)

    assert round_outcome_calls[0] == (0, constants.WIN)
    assert len(round_outcome_calls) == 1

def test_verify_round_end_cond_no_busts_push(monkeypatch, full_table):
    def fake_compare_hands(*args, **kwargs):
        return ('PUSH', constants.PUSH)

    monkeypatch.setattr('interface.compare_hands', fake_compare_hands)

    push_payout_calls = []
    def spy_push_payout(hand):
        push_payout_calls.append(hand)
        return 0

    monkeypatch.setattr('payout_calculator.push_payout', spy_push_payout)

    monkeypatch.setattr(
        'interface.is_new_round', 
        lambda *args, **kwargs: None
    )

    game.verify_round_end_cond(full_table)

    assert push_payout_calls[0].wager == 15.0

def test_verify_round_end_cond_multiple_iterations(monkeypatch, full_table):
    full_table.player.hands = [
        PlayerHand(
            cards=([Card('Spades', 10), Card('Diamonds', 9)])
        ), 
        PlayerHand(
            cards=([Card('Hearts', 10), Card('Diamonds', 2), Card('Clubs', 10)])
        ),
    ]

    full_table.dealer.cards = [
        Card('Hearts', 10), 
        Card('Diamonds', 2), 
        Card('Clubs', 10),
    ]
    
    def fake_is_bust(hand):
        if hand.cards[1].rank == 9:
            return False
        elif hand.cards[1].rank == 2:
            return True

    monkeypatch.setattr('conditions.is_bust', fake_is_bust)

    round_outcome_calls = []
    def spy_get_round_outcome_msg(i, flag):
        round_outcome_calls.append((i, flag))
        return i, flag

    monkeypatch.setattr(
        'interface.get_round_outcome_msg', 
        spy_get_round_outcome_msg)

    monkeypatch.setattr(
        'interface.is_new_round', 
        lambda *args, **kwargs: None
    )

    game.verify_round_end_cond(full_table)

    assert len(round_outcome_calls) == 2
    assert round_outcome_calls[0] == (0, constants.WIN)
    assert round_outcome_calls[1] == (1, constants.BUST)

# =======================
# MISC GAME TESTS.
# =======================
 
def test_get_player_wager(monkeypatch, full_table):
    monkeypatch.setattr('interface.wager_prompt', lambda _: 25.0)

    assert game._get_player_wager(full_table) == 25.0

def test_blackjack_round_done(monkeypatch, full_table):
    monkeypatch.setattr(game, '_get_player_wager', lambda *args, **kwargs: None)

    monkeypatch.setattr('actions.initial_round_deal', lambda *args, **kwargs: None)

    monkeypatch.setattr(game, 'exe_initial_cond', lambda _: True)

def test_blackjack_routing(monkeypatch, full_table):
    call_count = {'wager_calls': 0}

    def fake_get_player_wager(_):
        call_count['wager_calls'] += 1
        return 25.0

    monkeypatch.setattr(game, '_get_player_wager', fake_get_player_wager)

    monkeypatch.setattr(game, 'verify_round_end_cond', lambda _: False)
    monkeypatch.setattr(game, 'exe_initial_cond', lambda _: False)

    monkeypatch.setattr(game, 'exe_player_control', lambda _: None)
    monkeypatch.setattr(game, 'exe_dealer_control', lambda _: None)

    game.blackjack([], full_table.player.bank, 'Test')

    assert call_count['wager_calls'] == 1
