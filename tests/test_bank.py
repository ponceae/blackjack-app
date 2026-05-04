""" 
Tests for the `bank.py` module.

Ensures that the `Bank` class correctly initializes and validates the player's chips,
and enforces the minimum and maximum chip balance bounds.
"""

__author__ = 'Adrien P.'

import pytest

from bank import Bank
from constants import MAX_BANK
from data.constants import (
    BANK_BOUNDS_ERR_MSG, 
    BANK_INVALID_VALUE_ERR_MSG, 
    BANK_NEGATIVE_VALUE_ERR_MSG,
)

@pytest.mark.parametrize(
    'test_chips, expected_amount',
    [
        (15, 15.0),
        (1000, 1000.0),
        (34.5, 34.5),
        (14.99, 14.99),
        (0, 0.0),
        ('15', 15.0),
        ('7.5', 7.5),
    ],
)
def test_initial_bank_creation(test_chips, expected_amount):
    bank = Bank(test_chips)
    assert bank.chips == expected_amount

@pytest.mark.parametrize(
    'invalid_input, expected_err_msg',
    [
        (MAX_BANK + 0.01, BANK_BOUNDS_ERR_MSG,),
        (-3, BANK_BOUNDS_ERR_MSG),
        (-2.56, BANK_BOUNDS_ERR_MSG),
        ('4a', BANK_INVALID_VALUE_ERR_MSG),
        ('4.56num', BANK_INVALID_VALUE_ERR_MSG,),
    ],
    ids=[
        'invalid_count_a_big_float',
        'invalid_count_b_negative_int',
        'invalid_count_c_negative_float',
        'invalid_count_d_string_a',
        'invalid_count_e_string_b',
    ],
)
def test_init_raises_valueerror_on_invalid_input(invalid_input, expected_err_msg):
    with pytest.raises(ValueError, match=expected_err_msg):
        Bank(invalid_input)

@pytest.fixture
def bank() -> Bank:
    """Provide a `Bank` instance with a moderate balance."""
    return Bank(225.50)

@pytest.mark.parametrize(
    'add_amount, expected_balance',
    [
        (25, 250.5),
        (7.5, 233.0),
        (32.5, 258.0),
    ]
)
def test_adding_chips_to_bank(bank, add_amount, expected_balance):
    bank.chips += add_amount
    assert bank.chips == expected_balance

@pytest.mark.parametrize(
    'removal_amount, expected_balance',
    [
        (22.5, 203.0),
        (7.5, 218.0),
        (225.5, 0.0),
    ]
)
def test_removing_chips_from_bank(bank, removal_amount, expected_balance):
    bank.chips -= removal_amount
    assert bank.chips == expected_balance

@pytest.mark.parametrize(
    'set_amount, expected_balance',
    [
        (0, 0.0),
        (525.75, 525.75),
        (105.5, 105.5),
    ]
)
def test_setting_bank_chips(bank, set_amount, expected_balance):
    bank.chips = set_amount
    assert bank.chips == expected_balance

@pytest.mark.parametrize(
    'invalid_value, expected_err_msg',
    [
        (-5.5, BANK_NEGATIVE_VALUE_ERR_MSG),
        (-0.01, BANK_NEGATIVE_VALUE_ERR_MSG),
        ('number string', BANK_INVALID_VALUE_ERR_MSG),
        (None, BANK_INVALID_VALUE_ERR_MSG),
        ([], BANK_INVALID_VALUE_ERR_MSG),
    ],
    ids=[
        'invalid_value_a_negative_float_a',
        'invalid_value_b_negative_float_b',
        'invalid_value_c_string',
        'invalid_value_d_type_mismatch_a',
        'invalid_value_e_type_mismatch_b',
    ],
)
def test_bank_chips_setter_raises_valueerror_on_invalid_value(
        bank, 
        invalid_value, 
        expected_err_msg
):
    with pytest.raises(ValueError, match=expected_err_msg):
        bank.chips = invalid_value

@pytest.mark.parametrize(
    'chips, expected_display',
    [
        (15.0, 'Chips: $15.00'),
        (1000.0, 'Chips: $1,000.00'),
        (34.5, 'Chips: $34.50'),
        (14.99, 'Chips: $14.99'),
        (0.0, 'Chips: $0.00'),
    ]
)
def test_bank_chips_to_string(chips, expected_display):
    bank = Bank(chips)
    assert bank.to_string() == expected_display
