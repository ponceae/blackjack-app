""" 
Test data generator for the `conditions.py` module

Provides:
    - Generators for tuples containing two hands and their expected outcome. 
    - Generators for tuples containing a player and affordability of a wager.
    - Generators for a dealer hand to test validity of insurance purchases.
"""

__author__ = 'Adrien P.'

from entities import Card, DealerHand, Hand, PlayerHand, Outcome, OutcomeFlag

def generate_initial_deal_outcome_data() -> list[tuple[Hand, Hand, Outcome, str]]:
    """Test data for comparing a tables initial hands."""
    return [
        (
            PlayerHand(cards=[Card('Spades', 5), Card('Clubs', 4)]), 
            DealerHand(cards=[Card('Diamonds', 7), Card('Hearts', 5)]), 
            Outcome(),
            'no_outcome',
        ),
        (
            PlayerHand(cards=[Card('Spades', 'Ace'), Card('Clubs', 'Queen')]), 
            DealerHand(cards=[Card('Diamonds', 7), Card('Hearts', 5)]), 
            Outcome(flag=OutcomeFlag.PLAYER_BLACKJACK),
            'player_blackjack',
        ),
        (
            PlayerHand(cards=[Card('Spades', 5), Card('Clubs', 4)]), 
            DealerHand(cards=[Card('Diamonds', 'Ace'), Card('Hearts', 'King')]), 
            Outcome(flag=OutcomeFlag.DEALER_BLACKJACK),
            'dealer_blackjack',
        ),
        (
            PlayerHand(cards=[Card('Spades', 'Ace'), Card('Clubs', 'Jack')]), 
            DealerHand(cards=[Card('Diamonds', 'Ace'), Card('Hearts', 10)]), 
            Outcome(flag=OutcomeFlag.PUSH),
            'player_and_dealer_blackjack',
        ),
    ]
    
def generate_end_of_round_outcome_data() -> list[tuple[Hand, Hand, Outcome, str]]:
    """Test data for comparing table hands at the end of the round."""
    return [
        (
            PlayerHand(cards=[
                Card('Spades', 5), 
                Card('Clubs', 10), 
                Card('Clubs', 4),
            ]), 
            DealerHand(cards=[
                Card('Diamonds', 7), 
                Card('Hearts', 4), 
                Card('Clubs', 8),
            ]), 
            Outcome(flag=OutcomeFlag.PUSH),
            'round_push'
        ),
        (
            PlayerHand(cards=[
                Card('Spades', 5), 
                Card('Clubs', 4), 
                Card('Hearts', 10),
            ]), 
            DealerHand(cards=[
                Card('Diamonds', 8), 
                Card('Hearts', 5),
                Card('Diamonds', 5),
            ]), 
            Outcome(flag=OutcomeFlag.PLAYER_WIN),
            'player_wins_round',
        ),
        (
            PlayerHand(cards=[Card('Spades', 5), Card('Clubs', 4), Card('Clubs', 4)]), 
            DealerHand(cards=[Card('Diamonds', 10), Card('Hearts', 'Jack')]), 
            Outcome(flag=OutcomeFlag.DEALER_WIN),
            'dealer_wins_round'
        ),
    ]
def generate_dealerhands_and_balances() -> list[tuple[DealerHand, bool, float, str]]:
    """
    Test data for creating a dealer's hand and whether a player can purchase insurance
    with a given cost."""
    return [
        (
            DealerHand(cards=[Card('Clubs', 'Ace'), Card('Clubs', 2)]), 
            True, 
            400,
            'can_get_insurance_a',
        ),
        (
            DealerHand(cards=[Card('Clubs', 2), Card('Clubs', 'Ace')]), 
            False, 
            250,
            'cannot_get_insurance_a_invalid_cond',
        ),
        (
            DealerHand(cards=[Card('Clubs', 'Ace'), Card('Clubs', 2)]), 
            True, 
            100,
            'can_get_insurance_b',
        ),
        (
            DealerHand(cards=[Card('Clubs', 'Ace'), Card('Clubs', 2)]), 
            False, 
            500.01,
            'cannot_get_insurance_c_insufficient_funds',
        ),
        (
            DealerHand(cards=[Card('Clubs', 'Ace'), Card('Clubs', 2)]), 
            False, 
            -1,
            'cannot_get_insurance_d_negative_value',
        ),
        (
            DealerHand(cards=[Card('Clubs', 'Ace'), Card('Clubs', 2)]), 
            False, 
            0,
            'cannot_get_insurance_e_zero_value',
        ),
    ]
