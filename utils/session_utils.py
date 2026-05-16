""" 

"""

from flask import session
from entities import Outcome, Player, Table

__author__ = 'Adrien P.'

# ========================
# Table State Functions.
# ========================

def get_table() -> Table:
    """
    Create and return a `Table` instance from the Flask session, creating a new
    session entry if one does not yet exist.
    """
    table_dict = session.get('table')
    
    if table_dict:
        return Table.from_dict(table_dict)

    return Table(player=Player())

def save_table(table) -> None:
    """Save the current state of the `Table` to the Flask session."""
    session['table'] = table.to_dict()
    session.modified = True
    
def get_outcome() -> Outcome:
    outcome_dict = session.get('outcome')
    
    if outcome_dict:
        return Outcome.from_dict(outcome_dict)
    
    return Outcome()

def save_outcome(outcome: Outcome) -> None:
    session['outcome'] = outcome.to_dict()
    session.modified = True
