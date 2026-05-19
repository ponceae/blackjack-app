from functools import wraps

from flask import Flask, redirect, render_template, session, url_for
import json

from engine import actions, conditions
from entities import Outcome, OutcomeFlag, Player, PlayerHand, Table
from utils import session_utils

__author__ = 'Adrien P.'

app = Flask(__name__)
app.secret_key = 'some_top_secret_key'

def _game_active_required(func):
    @wraps(func)
    def _game_active_bouncer(*args, **kwargs):
        if not session.get('game_active'):
            return redirect('/')
        
        return func(*args, **kwargs)
    
    return _game_active_bouncer

def _force_stand_sequence(table: Table, curr_hand: PlayerHand):
    actions.handle_stand(table)
    
    outcome = conditions.compare_hands(curr_hand, table.dealer)
    
    return _end_round_sequence(table, outcome)

def _end_round_sequence(table: Table, outcome: Outcome):
    curr_hand = table.player.hands[table.player.active_hand_index]
    
    winnings = actions.handle_payout(curr_hand, outcome)
    
    session['winnings'] = winnings
    
    table.player.bank.balance += winnings
    
    session_utils.save_table(table)
    session_utils.save_outcome(outcome)
    
    return redirect(url_for('home'))

@app.route('/')
def home():
    # ===================
    # FOR DEBUGGING ONLY
    # ===================
    create_debug_section(session)
    
    return render_template(
        'index.html', 
        game_active=session.get('game_active', False), 
        outcome=session_utils.get_outcome(), 
        table=session_utils.get_table(),
        current_wager=session.get('current_wager', 0),
        winnings=session.get('winnings', 0),
    )

@app.route('/new_game', methods=['POST'])
def new_game():
    session['winnings'] = 0
    session['game_active'] = False
    
    return redirect(url_for('home'))

@app.route('/deal', methods=['POST'])
def deal():    
    table = Table(player=Player())
    table = actions.deal_initial_cards(table)

    _wager = session['current_wager']
    table.player.hands[table.player.active_hand_index].wager += _wager
    
    outcome = conditions.compare_initial_hands(table)

    if outcome.flag != OutcomeFlag.NONE:
        actions.dealer_turn(table)
        return _end_round_sequence(table, outcome)

    session['current_wager'] = 0
    session['game_active'] = True
    
    session_utils.save_table(table)
    session_utils.save_outcome(outcome)
    
    return redirect(url_for('home'))

@app.route('/hit', methods=['POST'])
@_game_active_required
def hit():
    table = session_utils.get_table()
    curr_hand = table.player.hands[table.player.active_hand_index]
    
    if curr_hand.value >= 21:
        return _force_stand_sequence(table, curr_hand)
    
    actions.hit_hand(table, table.player.current_hand)

    if curr_hand.value >= 21:
        return _force_stand_sequence(table, curr_hand)
        
    session_utils.save_table(table)
    return redirect(url_for('home'))
    
@app.route('/stand', methods=['POST'])
@_game_active_required
def stand():
    table = session_utils.get_table()
    curr_hand = table.player.hands[table.player.active_hand_index]
    
    actions.handle_stand(table)
    outcome = conditions.compare_hands(curr_hand, table.dealer)

    return _end_round_sequence(table, outcome)

@app.route('/bet/<float:amount>', methods=['POST'])
@app.route('/bet/<int:amount>', methods=['POST'])
def place_bet(amount):
    if 'current_wager' not in session:
        session['current_wager'] = 0
    
    session['current_wager'] += amount
    
    return redirect(url_for('home'))

@app.route('/remove/<float:amount>', methods=['POST'])
@app.route('/remove/<int:amount>', methods=['POST'])
def remove_bet(amount):    
    if session['current_wager'] - amount < 0:
        session['current_wager'] = 0
    else:
        session['current_wager'] -= amount

    return redirect(url_for('home'))

# ===================
# FOR DEBUGGING ONLY
# ===================
@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

def create_debug_section(session):
    debug_session = dict(session)
        
    print('== Current Session ==')
    print(json.dumps(debug_session, indent=4))
    
if __name__ == '__main__':
    app.run(debug=True)
    