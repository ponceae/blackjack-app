""" 
Tests for the `hand.py` module.

Validates Hand states, properties, and that the Hand subclasses, DealerHand and 
PlayerHand, correctly inherit Hand fields and that serialization and deserialization
creates correct data.
"""

import pytest

from data import hand_data
from entities.card import Card
from entities.hand import DealerHand, Hand, PlayerHand
from utils import validation 

# =========================================
# Private Helper Function Tests.
# -----------------------------------------
# Tests the _validate_type helper function.
# =========================================

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
        validation.validate_type(name, test_value, exp_type)

# ==========================
# Hand Initialization Tests.
# ========================== 

def test_hand_default_factory_creates_empty_list():
    hand_a = Hand()
    hand_b = Hand()
    
    assert hand_a == Hand(cards=[])
    assert hand_a is not hand_b

# ================================
# Hand Value and Hard Value Tests.
# ================================

@pytest.mark.parametrize(
    'test_cards, exp_opt_val, exp_hard_val',
    [
        (cards, opt_val, hard_val) 
        for (cards, _, opt_val, hard_val) in hand_data.generate_test_cards_large()
    ],
    ids=[tid[1] for tid in hand_data.generate_test_cards_large()]
)
def test_hand_optimal_and_hard_value(test_cards, exp_opt_val, exp_hard_val):
    hand = Hand(cards=test_cards)
    
    assert hand.value == exp_opt_val
    assert hand.hard_value == exp_hard_val

# ==================================================
# Hand State Tests.
# --------------------------------------------------
# Tests the is_bust, is_twenty_one, is_soft methods.
# ==================================================

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    [
        (cards, twenty_one) 
        for (cards, _, twenty_one, *_) 
        in hand_data.generate_test_cards_for_bust_and_twenty_one()
    ],
    ids=[
        'not_is_twenty_one_a',
        'is_twenty_one_a',
        'not_is_twenty_one_b',
        'is_twenty_one_b',
    ],
)
def test_hand_is_twenty_one(test_cards, expected_bool):
    hand = Hand(cards=test_cards)
    
    assert hand.is_twenty_one == expected_bool

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    [
        (cards, is_bust) 
        for (cards, is_bust, *_) 
        in hand_data.generate_test_cards_for_bust_and_twenty_one()
    ],
    ids=[
        'is_bust_a',
        'not_is_bust_a',
        'is_bust_b',
        'not_is_bust_b',
    ],
)
def test_hand_is_bust(test_cards, expected_bool):
    hand = Hand(cards=test_cards)
    
    assert hand.is_bust == expected_bool

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    [
        ([Card('Spades', 'Ace'), Card('Clubs', 4)], True),
        ([Card('Spades', 'Ace'), Card('Hearts', 9), Card('Diamonds', 6)], False),
        ([Card('Spades', 10), Card('Hearts', 7)], False),
        ([Card('Clubs', 'Ace'), Card('Spades', 'Ace'), Card('Diamonds', 4)], True)
    ],
    ids=[
        'is_soft_a',
        'not_is_soft_b',
        'not_is_soft_b',
        'is_soft_b',
    ],
)
def test_hand_is_soft(test_cards, expected_bool):
    hand = Hand(cards=test_cards)
    
    assert hand.is_soft == expected_bool

# =========================================
# Hand Serialization/Deserialization Tests.
# =========================================

@pytest.mark.parametrize('expected_hand, data_dict', hand_data.hand_mapping_pairs())
def test_from_dict_creates_hand_instance(expected_hand, data_dict):
    test_hand = Hand.from_dict(data_dict)
    
    assert test_hand.cards == expected_hand.cards

@pytest.mark.parametrize('hand, expected_data_dict', hand_data.hand_mapping_pairs())
def test_to_dict_creates_correct_hand_data_dict(hand, expected_data_dict):
    data_dict = hand.to_dict()

    assert data_dict == expected_data_dict
    
# =============================
# Other Hand Tests.
# -----------------------------
# Tests the add_cards method.
# ============================= 

@pytest.mark.parametrize(
    'hand, card, expected_length,',
    [
        (
            Hand(cards=[Card('Spades', 5), Card('Diamonds', 4)]), 
            Card('Clubs', 10), 
            3,
        ),
        (
            Hand(cards=[Card('Spades', 2), Card('Diamonds', 6), Card('Hearts', 3)]), 
            Card('Clubs', 10), 
            4,
        ), 
        (
            Hand(
                cards=[
                    Card('Spades', 2), 
                    Card('Diamonds', 6), 
                    Card('Hearts', 3), 
                    Card('Hearts', 2),
                ],
            ), 
            Card('Spades', 10),
            5,
        )
    ]
)
def test_add_card(hand, card, expected_length):
    hand.add_card(card)
    
    assert len(hand.cards) == expected_length
    assert hand.cards[-1] == card

# ===============================================
# DealerHand Serialization/Deserialization Tests.
# ===============================================

@pytest.mark.parametrize(
    'expected_hand, data_dict', 
    [
        (cards, data_dict) 
        for (cards, data_dict, *_) 
        in hand_data.dealerhand_mapping_pairs()
    ],
    ids=[
        (tids) for (*_, tids) in hand_data.dealerhand_mapping_pairs()
    ],
)
def test_from_dict_creates_dealerhand_instance(expected_hand, data_dict):
    test_hand = DealerHand.from_dict(data_dict)
    
    assert test_hand.cards == expected_hand.cards

@pytest.mark.parametrize(
    'hand, expected_data_dict',
    [
        (cards, data_dict) 
        for (cards, data_dict, *_) 
        in hand_data.dealerhand_mapping_pairs()
    ],
    ids=[
        (tids) for (*_, tids) in hand_data.dealerhand_mapping_pairs()
    ]
)
def test_to_dict_creates_correct_dealerhand_data_dict(hand, expected_data_dict):
    data_dict = hand.to_dict()

    assert data_dict == expected_data_dict

# ===============================================
# PlayerHand Serialization/Deserialization Tests.
# ===============================================

@pytest.mark.parametrize(
    'expected_hand, data_dict',
    [
        (cards, data_dict) 
        for (cards, data_dict, *_) 
        in hand_data.playerhand_mapping_pairs()
    ],
    ids=[
        (tid) for (*_, tid) in hand_data.playerhand_mapping_pairs()
    ]
)
def test_from_dict_creates_playerhand_instance(expected_hand, data_dict):
    test_hand = PlayerHand.from_dict(data_dict)
    
    assert test_hand.cards == expected_hand.cards

@pytest.mark.parametrize(
    'hand, expected_data_dict',
    [
        (cards, data_dict) 
        for (cards, data_dict, *_) 
        in hand_data.playerhand_mapping_pairs()
    ],
    ids=[
        (tid) for (*_, tid) in hand_data.playerhand_mapping_pairs()
    ]
)
def test_to_dict_creates_correct_playerhand_data_dict(hand, expected_data_dict):
    data_dict = hand.to_dict()

    assert data_dict == expected_data_dict

# ================================================================
# PlayerHand State Tests.
# ----------------------------------------------------------------
# Tests the can_split, is_initial_hand, and is_split_aces methods.
# ================================================================

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    [
        (cards, can_split) 
        for (cards, can_split, *_) 
        in hand_data.generate_test_cards_for_split_and_initial()
    ],
    ids=[
        'can_split_a',
        'cannot_split_a',
        'can_split_b',
        'cannot_split_b',
        'cannot_split_c'  
    ],
)
def test_hand_can_split(test_cards, expected_bool):
    hand = PlayerHand(cards=test_cards)
    
    assert hand.can_split == expected_bool

@pytest.mark.parametrize(
    'test_cards, expected_bool',
    [
        (cards, is_initial) 
        for (cards, _, is_initial, *_) 
        in hand_data.generate_test_cards_for_split_and_initial()
    ],    
    ids=[
        'is_initial_a',
        'not_is_initial_a',
        'is_initial_b',
        'not_is_initial_b',
        'is_initial_c',
    ]
)
def test_hand_is_initial_hand(test_cards, expected_bool):
    hand = PlayerHand(cards=test_cards)
    
    assert hand.is_initial_hand == expected_bool

@pytest.mark.parametrize(
    'hand, expected_bool',
    (
        (PlayerHand(cards=[Card('Spades', 'Ace'), Card('Clubs', 'Ace')]), True),
        (PlayerHand(cards=[Card('Spades', 'Ace'), Card('Clubs', 10)]), False),
        (PlayerHand(cards=[Card('Spades', 10), Card('Clubs', 10)]), False)
    )
)
def test_hand_is_split_aces(hand, expected_bool):
    assert hand.is_split_aces == expected_bool
