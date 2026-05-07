""" 
Tests for the `bank.py` module.

Ensures that the `Bank` class correctly initializes and validates the player's chips,
enforces the minimum and maximum chip balance bounds, and validates object packing
and unpacking.
"""

__author__ = 'Adrien P.'

import pytest
from typing import Any

from constants import MAX_BANK
from data.constants import (
    BANK_BOUNDS_ERR_MSG, 
    BANK_INVALID_VALUE_ERR_MSG, 
    BANK_NEGATIVE_VALUE_ERR_MSG,
)
from entities.bank import Bank

# ======================================
# Bank and Map Generators and Fixtures.
# ======================================

@pytest.fixture
def bank() -> Bank:
    """Provide a `Bank` instance with a moderate balance."""
    return Bank(225.50)

def _generate_bank_test_data() -> list[tuple[Bank, float, str, str]]:
    return [
        (Bank(15), 15.0, 'Chips: $15.00', "Bank(chips='15.0')"),
        (Bank(1000), 1000.0, 'Chips: $1,000.00', "Bank(chips='1000.0')"),
        (Bank(34.5), 34.5, 'Chips: $34.50', "Bank(chips='34.5')"),
        (Bank(14.99), 14.99, 'Chips: $14.99', "Bank(chips='14.99')"),
        (Bank(0), 0, 'Chips: $0.00', "Bank(chips='0.0')"),
        (Bank(float('25')), 25.0, 'Chips: $25.00', "Bank(chips='25.0')"),
        (Bank(float('7.5')), 7.5, 'Chips: $7.50', "Bank(chips='7.5')"),    
    ]

def _bank_mapping_pairs() -> list[tuple[Bank, dict[str, Any]]]:
    """Generate pairs of `Bank` instances and their expected {`chips`} dicts."""
    return [
        (bank, {'chips': bank.chips}) 
        for (bank, *_) in _generate_bank_test_data()
    ]

# ==========================
# Bank Initialization Tests.
# ==========================

@pytest.mark.parametrize(
    'bank, expected_chips',
    [(bank, chips) for (bank, chips, *_) in _generate_bank_test_data()], 
)
def test_init_creates_correct_bank_instance(bank, expected_chips):
    assert bank == Bank(expected_chips)

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

# =========================
# Bank Dunder Method Tests.
# =========================

def test_bank_equality():
    bank1 = Bank(15.0)
    bank2 = Bank(15.0)
    bank3 = Bank(34.5)
    
    assert bank1 == bank2
    
    assert bank1 != bank3
    
    assert bank1 != '15.0'

@pytest.mark.parametrize(
    'bank, expected_string',
    [(bank, string) for (bank, _, string, *_) in _generate_bank_test_data()]
)
def test_bank_string_display(bank, expected_string):
    assert str(bank) == expected_string

@pytest.mark.parametrize(
    'bank, expected_string',
    [(bank, string) for (bank, *_, string) in _generate_bank_test_data()],
)
def test_bank_string_debug_display(bank, expected_string):
    assert repr(bank) == expected_string

# ========================
# Bank Modification Tests.
# ========================

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

    assert bank == Bank(expected_balance)

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

    assert bank == Bank(expected_balance)

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

    assert bank == Bank(expected_balance)

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

# =========================================
# Bank Serialization/Deserialization Tests.
# =========================================

@pytest.mark.parametrize('expected_bank, data_dict', _bank_mapping_pairs())
def test_from_dict_creates_object(expected_bank, data_dict):
    test_bank = Bank.from_dict(data_dict)
    
    assert test_bank.chips == expected_bank.chips

@pytest.mark.parametrize('bank, expected_data_dict', _bank_mapping_pairs())
def to_dict_creates_data_dict(bank, expected_data_dict):
    data_dict = Bank.to_dict(bank)
    
    assert data_dict == expected_data_dict
