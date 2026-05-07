"""
Generator functions for the `test_hand.py` module.
"""

from entities.card import Card

def generate_test_cards_large() -> list[tuple[list[Card], str, int, int]]:
    """Provide a list of `Hand` test data."""
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