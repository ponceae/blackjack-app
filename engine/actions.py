"""
Blackjack game actions and calculations.
"""

__author__ = 'Adrien P.'

from entities import Card, Deck, Hand, PlayerHand, Table

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
    
    table.player.add_hand(PlayerHand())
    
    for i in range(4):
        card = table.deck.draw_card()
        
        if i % 2 == 0:
            table.player.hands[0].add_card(card)
        else:
            table.dealer.add_card(card)
            
    return table

# def initial_round_deal(table: Table) -> None:
#     """
#     Initialize a `PlayerHand` and a `DealerHand` on the table by dealing both 
#     two cards each.

#     Args:
#         table (Table): The table containing the `PlayerHand`, the `DealerHand`, and  
#             the deck of cards.
#     """
#     table.player.hands = [PlayerHand()]
#     table.dealer = DealerHand()

#     for i in range(4):
#         if not table.deck:
#             table.deck = create_and_shuffle()	

#         card = table.deck.pop()

#         if i % 2 == 0:
#             table.player.hands[0].cards.append(card)
#         else:
#             table.dealer.cards.append(card)

def hit_hand(table: Table, hand: Hand) -> Card:
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
    
    return card

def split_hand(table: Table) -> None:
    pass

# def create_split_hands(table: Table) -> None:
#     """
#     Create a new `PlayerHand` by popping a card from the first initial hand and
#     hitting both hands.

#     Args:
#         table (Table): The table containing the player's hand and the deck of cards.
#     """
#     table.player.hands.append(PlayerHand(cards=[table.player.hands[0].cards.pop()]))

#     for hand in table.player.hands:
#         hit_hand(table, hand)

