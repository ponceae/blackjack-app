"""
Blackjack game actions.

Contains functionality for initializing the Blackjack game and modifying the player's
and dealer's current hand.
"""

__author__ = 'Adrien P.'

from engine import conditions, payouts
from entities import Deck, Hand, Outcome, OutcomeFlag, PlayerHand, Table

def deal_initial_cards(table: Table) -> Table:
    """
    Initialize the game table with a `PlayerHand` and a `DealerHand` by dealing each 
    hand two cards each.
    
    Args:
        table (Table): The current game table containing the player's and dealer's
            hands and the game deck.
    
    Returns:
        Table: The newly initialized game table.
    """
    table.deck = Deck()  
    table.deck.shuffle()
    
    table.player.add_hand(PlayerHand(is_current=True))
    
    for i in range(4):
        card = table.deck.draw_card()
        
        if i % 2 == 0:
            table.player.hands[0].add_card(card)
        else:
            table.dealer.add_card(card)
            
    return table

def hit_hand(table: Table, hand: Hand) -> None:
    """
    Draw a card from the table's deck and add it to the provided hand.
    
    Args:
        table (Table): The current game table containing the deck and hand.
        hand (Hand): The hand to add the card to.
        
    Returns:
        Card: The card added to the hand.
    """
    card = table.deck.draw_card()
    hand.add_card(card)
    
def split_hand(table: Table) -> Table:
    """
    Create a new `PlayerHand` by removing a card from the first initial hand and
    drawing and adding a card to both hands.

    Args:
        table (Table): The table containing the player's hand and the game deck.

    Returns:
        Table: The updated game table.
    """
    table.player.add_hand(PlayerHand(cards=[table.player.hands[0].remove_card()]))

    for hand in table.player.hands:
        hand.add_card(table.deck.draw_card())

    return table

def handle_stand(table: Table) -> bool:
    """
    Return `True` if the player has hands left to play and increment
    the `active_hand_index`. If the player has no hands left, execute
    the dealer's turn.
    
    Args:
        table (Table): The current game table containing the player's hands.
    
    Returns:
        (bool): `True` if the player has hands left to play, `False` otherwise.
    """
    if table.player.active_hand_index < table.player.count() - 1:
        table.player.active_hand_index += 1
        return True
    
    table = dealer_turn(table)
    return False

def _generate_payout_map(player_hand) -> dict[OutcomeFlag, float]:
    return {
        OutcomeFlag.NONE: 0.0,
        OutcomeFlag.PLAYER_WIN: payouts.standard_payout(player_hand),
        OutcomeFlag.PLAYER_BLACKJACK: payouts.blackjack_payout(player_hand),
        OutcomeFlag.DEALER_WIN: 0.0,
        OutcomeFlag.DEALER_BLACKJACK: 0.0,
        OutcomeFlag.PUSH: payouts.push_payout(player_hand),
        OutcomeFlag.LOSE: 0.0,
    }

def handle_payout(player_hand: PlayerHand, outcome: Outcome) -> float:
    payout_dict = _generate_payout_map(player_hand)
    
    payout = payout_dict[outcome.flag]
    
    return payout

def dealer_turn(table: Table) -> Table:
    """
    Change the dealer's `is_face_up` field to `True` and draw cards until
    the dealer's hand value reaches or exceeds 17.
    
    Args: 
        table (Table): The current game table containing the dealer's cards.
        
    Returns:
        Table: The updated game table.
    """
    table.dealer.is_face_up = True
    
    while table.dealer.value < 17:
        card = table.deck.draw_card()
        table.dealer.add_card(card)
        
    return table
