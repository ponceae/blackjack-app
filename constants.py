"""
Global constants and configuration values for Blackjack.

Provides a single source for static game data, including:
    - Card definitions (card ranks, suits, and numeric values).
    - Monetary settings (wager and bank limits and configuration).
"""

__author__ = 'Adrien P.'

# =====================================
# Card Constants (Scoring and Strings).
# =====================================

ACE = 'Ace'
ACE_ALT_VALUE = 1
DEFAULT_ACE_VALUE = 11
FACE_CARD_VALUE = 10

CARD_RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
CARD_SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
CARD_SUIT_SYMBOLS = {
    'Clubs': '♣', 
    'Diamonds': '♦', 
    'Hearts': '♥', 
    'Spades': '♠',
}
NAMED_CARD_RANKS = ['Ace', 'Jack', 'Queen', 'King']

# ===========================
# Wager and Bank Information. 
# ===========================

MAX_STARTING_CAP = 1000000 # 1 Million

MIN_WAGER = 15
MAX_WAGER = 1000000 # 1 Million
