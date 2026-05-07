""" 
Tests for the `hand.py` module.
"""

import pytest

from data.hand_data import generate_test_cards_large
from entities.card import Card
from entities.hand import _validate_type, Hand

# ===========
# Generators.
# ===========

def gene

# ==============================
# Private Helper Function Tests.
# ==============================

@pytest.mark.parametrize(
    'name, test_value, exp_type, exp_err_msg',
    [
        (
            'Test A', 
            '5', 
            (int, float), 
            'Expected `Test A` to be `int or float`, got str',
        ),
        (
            'Test B',
            ['Test B', 999],
            str,
            'Expected `Test B` to be `str`, got list',    
        ),
        (
            'Test C',
            {'Test C': 999},
            bool,
            'Expected `Test C` to be `bool`, got dict',
        ),
        (
            'Test D',
            True,
            list,
            'Expected `Test D` to be `list`, got bool',
        ),
    ],
    ids=[
        'int_or_float_got_str_err',
        'str_got_list_err',
        'bool_got_dict_err',
        'list_got_bool_err',
    ]
)
def test_validate_type_shows_correct_err_msg(name, test_value, exp_type, exp_err_msg):
    with pytest.raises(TypeError, match=exp_err_msg):
        _validate_type(name, test_value, exp_type)

# ==========================
# Hand Initialization Tests.
# ========================== 

def test_hand_default_factory_creates_empty_list():
    hand_a = Hand()
    hand_b = Hand()
    
    assert hand_a == Hand(cards=[])
    assert hand_a is not hand_b

# =================
# Hand Value Tests.
# =================

@pytest.mark.parametrize(
    'test_cards, exp_opt_val, exp_hard_val',
    [
        (cards, opt_val, hard_val) 
        for (cards, _, opt_val, hard_val) in generate_test_cards_large()
    ],
    ids=[tid[1] for tid in generate_test_cards_large()]
)
def test_hand_optimal_and_hard_value(test_cards, exp_opt_val, exp_hard_val):
    hand = Hand(cards=test_cards)
    
    assert hand.value == exp_opt_val
    assert hand.hard_value == exp_hard_val

# # =================
# # Hand State Tests.
# # =================

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    zip(_generate_test_cards_small(), [True, True, False, False]),
    ids=[
        'can_split_a',
        'can_split_b',
        'cannot_split_a',
        'cannot_split_b',  
    ],
)
def test_hand_can_split(test_cards, expected_bool):
    hand = Hand(cards=test_cards)
    
    assert hand.can_split == expected_bool

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    zip(_generate_test_cards_small(), [True, True, True, False]),
    ids=
    [
        'is_initial_a',
        'is_initial_b',
        'is_initial_c',
        'not_is_initial_a',
    ]
)
def test_hand_is_initial_hand(test_cards, expected_bool):
    hand = Hand(cards=test_cards)
    
    assert hand.is_initial_hand == expected_bool

# @pytest.mark.parametrize(
#     'test_cards, expected_bool',
#     zip(
#         _generate_test_cards_for_bust_and_twenty_one(),
#         [False, True, False, True, False, False],
#     ),
#     ids=[
#         'not_is_twenty_one_a',
#         'is_twenty_one_a',
#         'not_is_twenty_one_b',
#         'is_twenty_one_b',
#         'not_is_twenty_one_c',
#         'not_is_twenty_one_d',
#     ],
# )
# def test_hand_is_twenty_one(test_cards, expected_bool):
#     hand = Hand(cards=test_cards)
    
#     assert hand.is_twenty_one == expected_bool

# @pytest.mark.parametrize(
#     'test_cards, expected_bool',
#     zip(
#         _generate_test_cards_for_bust_and_twenty_one(),
#         [True, False, False, False, False, True],
#     ),
#     ids=[
#         'is_bust_a',
#         'not_is_bust_a',
#         'not_is_bust_b',
#         'not_is_bust_c',
#         'not_is_bust_d',
#         'is_bust_b',
#     ],
# )
# def test_hand_is_bust(test_cards, expected_bool):
#     hand = Hand(cards=test_cards)
    
#     assert hand.is_bust == expected_bool

# @pytest.mark.parametrize(
#     'test_cards, expected_bool',
#     zip(
#         _generate_test_cards_large(),
#         [
#             False, False, False, True, False, True, False, False, False, False, False, 
#             True, False, False
#         ]
#     )
# )
# def test_hand_is_soft(test_cards, expected_bool):
#     hand = Hand(cards=test_cards)
    
#     assert hand.is_soft == expected_bool