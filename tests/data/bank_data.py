""" 
Test data generator and and mapping logic for the `test_bank.py` module.

Provides:
    - Bank object generator with string representations.
    - Dictonary factory for `from_dict`/`to_dict`.
"""

__author__ = 'Adrien P.'

from typing import Any

from entities.bank import Bank

def generate_bank_test_data() -> list[tuple[Bank, float, str, str]]:
    """
    Test data for the `Bank` balance, and the hand's optimal and hard values. Also
    contains the TID (test ID) for each tuple.
    
    (Bank(), str(), repr())
    """
    return [
        (Bank(15), 15.0, 'Balance: $15.00', "Bank(balance='15.0')"),
        (Bank(1000), 1000.0, 'Balance: $1,000.00', "Bank(balance='1000.0')"),
        (Bank(34.5), 34.5, 'Balance: $34.50', "Bank(balance='34.5')"),
        (Bank(14.99), 14.99, 'Balance: $14.99', "Bank(balance='14.99')"),
        (Bank(0), 0, 'Balance: $0.00', "Bank(balance='0.0')"),
        (Bank(float('25')), 25.0, 'Balance: $25.00', "Bank(balance='25.0')"),
        (Bank(float('7.5')), 7.5, 'Balance: $7.50', "Bank(balance='7.5')"),    
    ]

def bank_mapping_pairs() -> list[tuple[Bank, dict[str, Any]]]:
    """Generate pairs of `Bank` instances and their expected {`balance`} dicts."""
    return [
        (bank, {'balance': bank.balance}) 
        for (bank, *_) in generate_bank_test_data()
    ]
