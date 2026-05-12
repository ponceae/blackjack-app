""" 
Tests for the `models.py` module.

Ensures that serialization and deserialization create the correct `Insurance` and 
`Outcome` instances and data dictionaries. Also validates that reset defaults back to
their respective default factories.
"""

__author__ = 'Adrien P.'

import pytest

from data import models_data as md
from entities import Insurance, Outcome, OutcomeFlag

# ==========================
# Insurance Dataclass Tests.
# ==========================

@pytest.mark.parametrize('exp_insurance, data_dict', md.insurance_mapping_pairs())
def test_from_dict_creates_insurance_instance(exp_insurance, data_dict):
    test_insurance = Insurance.from_dict(data_dict)
    
    assert test_insurance == exp_insurance

@pytest.mark.parametrize('insurance, exp_data_dict', md.insurance_mapping_pairs())
def test_to_dict_creates_insurance_data_dict(insurance, exp_data_dict):
    data_dict = insurance.to_dict()
    
    assert data_dict == exp_data_dict

def test_insurance_reset_to_default_factory():
    insurance = Insurance(True, True, 15.0, 7.5)
    
    insurance.reset()
    
    assert insurance == Insurance()

# ========================
# Outcome Dataclass Tests.
# ========================

@pytest.mark.parametrize('expected_outcome, data_dict', md.outcome_mapping_pairs())
def test_from_dict_creates_outcome_instance(expected_outcome, data_dict):
    test_outcome = Outcome.from_dict(data_dict)
    
    assert test_outcome == expected_outcome

@pytest.mark.parametrize('outcome, expected_data_dict', md.outcome_mapping_pairs())
def test_to_dict_creates_outcome_data_dict(outcome, expected_data_dict):
    data_dict = outcome.to_dict()
    
    assert data_dict == expected_data_dict

def test_outcome_reset_to_default_factory():
    outcome = Outcome(OutcomeFlag.PLAYER_BLACKJACK, 32.5)
    
    outcome.reset()
    
    assert outcome == Outcome()
