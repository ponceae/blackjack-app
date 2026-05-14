""" 

"""

from flask import session
from entities import Player, Table

__author__ = 'Adrien P.'

def get_table() -> Table:
    table_dict = session.get('table')
    
    if table_dict:
        return Table.from_dict(table_dict)

    return Table(player=Player())

def save_table(table) -> None:
    session['table'] = table.to_dict()
