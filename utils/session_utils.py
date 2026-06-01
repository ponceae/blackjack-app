""" 
This module provides functionality for modifying and pulling data from a 
Flask session.
"""

from flask import session
from entities import Insurance, Outcome, Player, Table

__author__ = 'Adrien P.'

# ========================
# Table State Functions.
# ========================

def get_table() -> Table:
    """
    Create and return a `Table` instance from the Flask session, creating a new
    session entry if one does not yet exist.
    
    Returns:
        Table: A new Table instance.
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
    """ 
    Create and return an `Outcome` instance from the Flask session, creating a new
    session entry if one does not yet exist.
    
    Returns:
        Outcome: A new Outcome instance.
    """
    outcome_dict = session.get('outcome')
    
    if outcome_dict:
        return Outcome.from_dict(outcome_dict)
    
    return Outcome()

def save_outcome(outcome: Outcome) -> None:
    """Save the current state of the `Outcome` to the Flask session."""
    session['outcome'] = outcome.to_dict()
    session.modified = True

def get_insurance() -> Insurance:
    """ 
    Create and return an `Insurance` instance from the Flask session, creating a new
    session entry if one does not yet exist.
    
    Returns:
        Insurance: A new Insurance instance.
    """
    insurance_dict = session.get('insurance')
    
    if insurance_dict:
        return Insurance.from_dict(insurance_dict)
    
    return Insurance()
    
def save_insurance(insurance: Insurance) -> None:
    """Save the current state of the `Insurance` instance to the Flask session."""
    session['insurance'] = insurance.to_dict()
    session.modified = True
    