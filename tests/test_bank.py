""" 
Tests for the `bank.py` module.

Ensures that the `Bank` class correctly initializes and validates the player's chips,
enforces the minimum and maximum chip balance bounds, and validates object packing
and unpacking.
"""

__author__ = 'Adrien P.'

import pytest

from constants import MAX_STARTING_CAP
from data import bank_data
from data.metadata import (
    BANK_BOUNDS_ERR_MSG, 
    BANK_INVALID_VALUE_ERR_MSG, 
    BANK_NEGATIVE_VALUE_ERR_MSG,
)
from entities.bank import Bank

@pytest.fixture
def bank() -> Bank:
    """Provide a `Bank` instance with a moderate balance."""
    return Bank(225.50)

# ==========================
# Bank Initialization Tests.
# ==========================

@pytest.mark.parametrize(
    'bank, expected_balance',
    [(bank, balance) for (bank, balance, *_) in bank_data.generate_bank_test_data()], 
)
def test_init_creates_correct_bank_instance(bank, expected_balance):
    assert bank == Bank(expected_balance)

@pytest.mark.parametrize(
    'invalid_input, expected_err_msg',
    [
        (MAX_STARTING_CAP + 0.01, BANK_BOUNDS_ERR_MSG,),
        (-3, BANK_NEGATIVE_VALUE_ERR_MSG),
        (-2.56, BANK_NEGATIVE_VALUE_ERR_MSG),
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
    [(bank, string) for (bank, _, string, *_) in bank_data.generate_bank_test_data()]
)
def test_bank_string_display(bank, expected_string):
    assert str(bank) == expected_string

@pytest.mark.parametrize(
    'bank, expected_string',
    [(bank, string) for (bank, *_, string) in bank_data.generate_bank_test_data()],
)
def test_bank_string_debug_display(bank, expected_string):
    assert repr(bank) == expected_string

# ==================================
# Bank Modification Tests.
# ----------------------------------
# Test the bank.chips setter method.
# (addition, removal, & setting).
# ==================================

@pytest.mark.parametrize(
    'add_amount, expected_balance',
    [
        (25, 250.5),
        (7.5, 233.0),
        (32.5, 258.0),
    ]
)
def test_adding_chips_to_bank(bank, add_amount, expected_balance):
    bank.balance += add_amount

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
    bank.balance -= removal_amount

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
    bank.balance = set_amount

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
        bank.balance = invalid_value

# =========================================
# Bank Serialization/Deserialization Tests.
# =========================================

@pytest.mark.parametrize('expected_bank, data_dict', bank_data.bank_mapping_pairs())
def test_from_dict_creates_bank_instance(expected_bank, data_dict):
    test_bank = Bank.from_dict(data_dict)
    
    assert test_bank.balance == expected_bank.balance

@pytest.mark.parametrize('bank, expected_data_dict', bank_data.bank_mapping_pairs())
def test_to_dict_creates_correct_data_dict(bank, expected_data_dict):
    data_dict = Bank.to_dict(bank)
    
    assert data_dict == expected_data_dict
