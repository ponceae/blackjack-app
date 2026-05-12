""" 
Test generator and mapping logic for the `models.py` module.

Provides:
    - Insurance object generator.
    - Outcome object generator.
    - Factory for insurance dictionaries.
    - Factory for outcome dictionaries.
"""

from typing import Any

from entities.models import Insurance, Outcome, OutcomeFlag

__author__ = 'Adrien P.'

def _generate_insurance_objects() -> list[Insurance]:
    """Provide a list of `Insurance` objects."""
    return [
        Insurance(cost=7.5),
        Insurance(active=True, payout=15.0, cost=7.5),
        Insurance(cost=27.5),
        Insurance(active=True, win=True, payout=55.0, cost=27.5),
        Insurance(cost=17.5),
        Insurance(active=True, payout=45.0, cost=22.5),
        Insurance(cost=37.5),
    ]

def insurance_mapping_pairs() -> list[tuple[Insurance, dict[str, Any]]]:
    """Generate pairs of `Insurance` {'active', 'win', 'payout', 'cost'} dicts."""
    return [
        (
            insurance, {
                'active': insurance.active, 
                'win': insurance.win, 
                'payout': insurance.payout, 
                'cost': insurance.cost
            },
        )
        for insurance in _generate_insurance_objects()
    ]

def _generate_outcome_objects() -> list[Outcome]:
    """Provide a list of `Outcome` objects."""
    return [
        Outcome(),
        Outcome(flag=OutcomeFlag.PLAYER_WIN, payout=22.5),
        Outcome(flag=OutcomeFlag.PLAYER_BLACKJACK, payout=32.5),
        Outcome(flag=OutcomeFlag.DEALER_WIN),
        Outcome(flag=OutcomeFlag.DEALER_BLACKJACK),
        Outcome(flag=OutcomeFlag.PUSH, payout=15.0),
        Outcome(),
    ]

def outcome_mapping_pairs() -> list[tuple[Outcome, dict[str, Any]]]:
    """Generate pairs of `Outcome` {'flag', 'payout'} dicts."""
    return [
        (outcome, {'flag': outcome.flag, 'payout': outcome.payout})
        for outcome in _generate_outcome_objects()
    ]
