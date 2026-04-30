""" 
Shared fixtures and configuration for the test suite.

Contains globally available testing utilities, including:
- Mock generators for console inputs
"""

__author__ = 'Adrien P.'

import pytest

@pytest.fixture
def mock_inputs(monkeypatch):
    """ 
    Provide a callable to mock sequential `input()` responses during testing.
    
    Returns a function that takes an iteration of input values. Each time `input` 
    called, it takes the next value from the iterable, failing the test if the iterable
    is empty.
    """
    def _mock_inputs(values):

        inputs = iter(values)
        
        def mock_input(prompt):
            try:
                return next(inputs)
            except StopIteration:
                pytest.fail(f'Test ran out of mock inputs.\nLast Prompt: {prompt}\n')

        monkeypatch.setattr('builtins.input', mock_input)

    return _mock_inputs
