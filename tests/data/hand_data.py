"""
Test data generator and mapping logic for the `test_hand.py` module.

Provides:
    - Raw card set generators and its TIDs.
    - Remapped tuples for DealerHand and PlayerHand.
    - Dictionary factories for testing `from_dict`/`to_dict`.
"""

__author__ = 'Adrien P.'

from typing import Any

from entities.card import Card
from entities.hand import DealerHand, Hand, PlayerHand

def generate_test_cards_large() -> list[tuple[list[Card], str, int, int]]:
    """
    Test data for the `Hand` cards, and the hand's optimal and hard values. Also
    contains the TID (test ID) for each tuple.
    
    (list[Card]: cards, str: tid, int: value, int: hard_value)
    """
    return [
        (
            [Card('Clubs', 2), Card('Hearts', 3), Card('Spades', 4)], 
            'two_pip_cards', 
            9, 
            9,
        ),
        (
            [Card('Clubs', 10), Card('Hearts', 'Jack')], 
            'one_pip_card_one_face_card', 
            20, 
            20,
        ),
        (
            [Card('Clubs', 7), Card('Hearts', 8), Card('Spades', 9)],
            'three_pip_cards',
            24,
            24,
        ),
        (
            [Card('Clubs', 'Ace'), Card('Hearts', 5)],
            'one_ace_card_one_pip_card_a',
            16,
            6,
        ),
        (
            [Card('Clubs', 'Ace'), Card('Spades', 'King')],
            'one_ace_card_one_face_card',
            21,
            11,
        ),
        (
            [Card('Clubs', 'Ace'), Card('Hearts', 2), Card('Spades', 3)],
            'one_ace_card_two_pip_cards_a',
            16,
            6,
        ),
        (
            [Card('Clubs', 2), Card('Hearts', 9), Card('Spades', 'Ace')],
            'two_pip_cards_one_ace_card',
            12,
            12,
        ),
        (
            [Card('Clubs', 'Ace'), Card('Hearts', 'Ace')],
            'two_ace_cards',
            12,
            2,
        ),
        (
            [Card('Clubs', 'Ace'), Card('Hearts', 'Ace'), Card('Spades', 9)],
            'two_ace_cards_one_pip_card',
            21,
            11,
        ),
        (
            [Card('Clubs', 'Ace'), Card('Hearts', 'Ace'), Card('Spades', 'King')],
            'two_ace_cards_one_face_card',
            12,
            12,
        ),
        (
            [
                Card('Clubs', 'Ace'), 
                Card('Hearts', 'Ace'), 
                Card('Spades', 'Ace'), 
                Card('Diamonds', 'Ace'),
            ],
            'four_ace_cards',
            14,
            4,
        ),
        (
            [Card('Clubs', 'Ace'), Card('Hearts', 9)],
            'one_ace_card_one_pip_card_b',
            20,
            10,
        ),
        (
            [Card('Clubs', 'Ace'), Card('Hearts', 4), Card('Spades', 6)],
            'one_ace_card_two_pip_cards_b',
            21,
            11,
        ),
        (
            [Card('Clubs', 'Ace'), Card('Hearts', 5), Card('Spades', 6)],
            'one_ace_card_two_pip_cards_c',
            12,
            12
        ),
    ]
    
def generate_dealer_or_player_test_data(hand_type: str) -> list[tuple[Any, ...]]:    
    """
    Test data that uses provided cards generator to create a new tuple with 
    DealerHand or PlayerHand fields.
    """
    test_data = []   
    for i, (cards, tid, *_) in enumerate(generate_test_cards_large()):

        test_bool = (i % 2 == 1)
        
        test_float = (10 * i) / 2
        
        if hand_type == 'dealer':
            test_data.append((cards, tid, test_bool))
        
        elif hand_type == 'player':
            test_data.append((cards, tid, test_float, test_float, test_bool))
    
    return test_data

def dealerhand_mapping_pairs() -> list[tuple[DealerHand, dict, str]]:
    """Generate pairs of `DealerHand` {'is_face_up'} dicts."""
    dealerhand_mappings = []
        
    for (_cards, tid, face_up) in generate_dealer_or_player_test_data('dealer'):
        
        hand = DealerHand(cards=_cards, is_face_up=face_up)
        
        data = {
            'cards': [c.to_dict() for c in _cards],
            'is_face_up': face_up
        }
        
        dealerhand_mappings.append((hand, data, tid))
    
    return dealerhand_mappings

PlayerHandData = list[tuple[PlayerHand, list[Card], float, float, bool]]

def playerhand_mapping_pairs() -> PlayerHandData:
    """
    Generate pairs of `PlayerHand` {'wager', 'insurance_wager', 'is_current'} dicts.
    """
    playerhand_mappings = []
    
    for (
        _cards, 
        tid, 
        _wager, 
        _insurance_wager, 
        current
    ) in generate_dealer_or_player_test_data('player'):
        
        hand = PlayerHand(
            cards=_cards, 
            wager=_wager, 
            insurance_wager=_insurance_wager, 
            is_current=current
        )
        
        data = {
            'cards': [c.to_dict() for c in _cards],
            'wager': _wager,
            'insurance_wager': _insurance_wager,
            'is_current': current,
        }

        playerhand_mappings.append((hand, data, tid))

    return playerhand_mappings

HandTestData_A = list[tuple[list[Card], bool, bool]]

def generate_test_cards_for_split_and_initial() -> HandTestData_A:
    """
    Test data for `Hand` split logic and initial hand state. 
    (list[Card]: cards, bool: can_split, bool: is_initial_hand).
    """
    return [
        ([Card('Spades', 5), Card('Hearts', 5)], True, True),
        ([Card('Clubs', 4), Card('Spades', 7), Card('Clubs', 3)], False, False),
        ([Card('Spades', 6), Card('Diamonds', 6)], True, True),
        ([Card('Clubs', 3), Card('Spades', 5), Card('Clubs', 2)], False, False),
        ([Card('Diamonds', 4), Card('Spades', 6)], False, True),
    ]

HandTestData_B = list[tuple[list[Card], bool, bool]]

def generate_test_cards_for_bust_and_twenty_one() -> HandTestData_B:
    """
    Test data for `Hand` bust and twenty one logic.
    (list[Card]: cards, bool: is_bust, bool: is_twenty_one).
    """
    return [
        ([Card('Clubs', 7), Card('Spades', 5), Card('Hearts', 'King')], True, False),
        ([Card('Clubs', 'Ace'), Card('Hearts', 10)], False, True),
        ([Card('Clubs', 10), Card('Hearts', 4), Card('Clubs', 10)], True, False),
        ([Card('Spades', 'Queen'), Card('Diamonds', 'Ace')], False, True)
    ]

def hand_mapping_pairs() -> list[tuple[Hand, dict[str, Any]]]:
    """Generate pairs of `Hand` instances and their expected {`cards`} dicts."""
    return [
        (Hand(cards=_cards), {'cards': [c.to_dict() for c in _cards]})
        for (_cards, *_) in generate_test_cards_large()
    ]
