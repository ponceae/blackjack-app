""" 
Global module that provides a validator function for the serialization of the 
Blackjack entities.
"""

__author__ = 'Adrien P.'

from typing import Any

def validate_type(field_name: str, value: Any, expected_type: type | tuple) -> None:
    """
    Enforce strict type checking during deserialization.
    
    Args:
        field_name (str): The name of the expected attribute field.
        value (Any): The current value to validate.
        expected_type (type | tuple): The expected variable type of `value`.
    """
    if not isinstance(value, expected_type):
        if isinstance(expected_type, tuple):
            type_names = ' or '.join(t.__name__ for t in expected_type)
        else:
            type_names = expected_type.__name__
            
        raise TypeError(
            f'Expected `{field_name}` to be `{type_names}`, '
            f'got {type(value).__name__}'
        )
