""" 
Global constants for the testing modules, such as error message displays.
"""

__author__ = 'Adrien P.'

from constants import MAX_BANK

BANK_BOUNDS_ERR_MSG = (
    f'Invalid value, `chips` must be a number between 0 and {MAX_BANK:,.2f}'
)
BANK_INVALID_VALUE_ERR_MSG = 'Invalid value, `value` must be a number.'
BANK_NEGATIVE_VALUE_ERR_MSG = 'Invalid value, `value` is less than 0.'

CARD_INVALID_SUIT_ERR_MSG = (
    "Invalid suit, `suit` must be one of: "
    "'Clubs', 'Diamonds', 'Hearts', 'Spades'."
)
CARD_INVALID_RANK_ERR_MSG = (
    "Invalid rank, `rank` must be one of: "
    "'2' through '10', 'Jack', 'King', 'Queen', 'Ace'."
)
