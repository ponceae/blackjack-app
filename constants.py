"""
Global constants and configuration values for Blackjack.

Provides a single source for static game data, including:
- Card definitions (card ranks, suits, and numeric values)
- Game logic variables (user inputs, round outcomes, and timer messages)
- Monetary settings (wager and bank limits and configuration)
- File system constants (JSON file paths)
"""

__author__ = 'Adrien P.'

from pathlib import Path

# ===============
# CARD CONSTANTS
# ===============

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

# ==========
# I/O FLAGS
# ==========

HIT = 'H'
STAND = 'S'

NO = 'N'
YES = 'Y'

BUST = 'B'
DOUBLE = 'D'

WIN = 'W'

# ==============
# OUTCOME FLAGS
# ==============

PLAYER_WIN = 1
DEALER_WIN = 2
PUSH = 3

# ============
# TIMER FLAGS
# ============

INITIAL = 1
PLAYER = 2
SWITCH_TURN = 3
DEALER = 4
CHECK = 5
SHOW = 6
BROKE = 7

TIMER_MESSAGES = {
    1: 'Dealer is peeking... {}',  
    2: 'Switching active hand... {}',  
    3: 'Switching to dealer... {}',  
    4: 'Dealer is hitting... {}',  
    5: 'Comparing hand values... {}',  
    6: 'Dealer is flipping card... {}', 
    7: 'You cannot afford that... {}',
}

# ==========
# JSON INFO
# ==========

FILE_PATH = Path(__file__).parent / 'save_data.json'
PLAYER_CHIPS = 'player_chips'

# ==============
# WAGERS & BANK 
# ==============

MAX_BANK = 1000000 # 1 Million

MIN_WAGER = 15
MAX_WAGER = 1000000 # 1 Million

# ===============
# MISCELLANEOUS
# ===============

ROMAN_NUMERALS = {1: 'I', 2: 'II'}
