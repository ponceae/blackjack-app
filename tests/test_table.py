""" 
Tests for the `table.py` module.

Ensures that serialization and deserialization create the correct `Table` instance and
data dictionary.
"""

__author__ = 'Adrien P.'

import pytest 

from data import table_data
from entities.table import Table

@pytest.mark.parametrize(
    'expected_table, data_dict',
    table_data.table_mapping_pairs()
)
def test_from_dict_creates_table_instance(expected_table, data_dict):
    test_table = Table.from_dict(data_dict)
    
    assert test_table == expected_table

@pytest.mark.parametrize(
    'table, expected_data_dict',
    table_data.table_mapping_pairs()
)
def test_to_dict_creates_correct_data_dict(table, expected_data_dict):
    data_dict = table.to_dict()
    
    assert data_dict == expected_data_dict
