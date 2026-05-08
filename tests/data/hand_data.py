"""
Generator functions for the `test_hand.py` module.
"""

from entities.card import Card
from entities.hand import DealerHand, PlayerHand

def generate_test_cards_large() -> list[tuple[list[Card], str, int, int]]:
    """
    Provide a list of `Hand` test data.
    
    Organized as (Hand.cards, Test ID, Optimal Hand Value, Hard Hand Value).
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
    
def generate_dealer_or_player_test_data(hand_type):    
    test_data = []   
    for i, (cards, tid, *_) in enumerate(generate_test_cards_large()):

        test_bool = (i % 2 == 1)
        
        test_float = (10 * i) / 2
        
        if hand_type == 'dealer':
            test_data.append((cards, tid, test_bool))
        
        
        elif hand_type == 'player':
            test_data.append((cards, tid, test_float, test_float, test_bool))
    
    return test_data

def dealerhand_mapping_pairs():
    dealerhand_mappings = []
        
    for (_cards, tid, face_up) in generate_dealer_or_player_test_data('dealer'):
        
        hand = DealerHand(cards=_cards, is_face_up=face_up)
        
        data = {
            'cards': [c.to_dict() for c in _cards],
            'is_face_up': face_up
        }
        
        dealerhand_mappings.append((hand, data, tid))
    
    return dealerhand_mappings

def playerhand_mapping_pairs():
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
