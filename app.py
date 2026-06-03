from functools import wraps
import os

from flask import Flask, redirect, render_template, session, url_for

from engine import actions, conditions
from entities import OutcomeFlag, Player, Table
from utils import session_utils

__author__ = 'Adrien P.'

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

def _game_active_required(func):
    @wraps(func)
    def _game_active_bouncer(*args, **kwargs):
        if not session.get('game_active'):
            return redirect('/')
        
        return func(*args, **kwargs)
    
    return _game_active_bouncer

def _end_round_sequence(table: Table):    
    winnings = 0
    side_winnnigs = 0
    insurance = session_utils.get_insurance()
        
    if insurance.active and table.dealer.is_twenty_one:
        insurance.win = True
        side_winnnigs += insurance.payout
        
    for hand in table.player.hands:
        outcome = conditions.compare_initial_hands(table)
        
        if outcome.flag == OutcomeFlag.NONE:
            outcome = conditions.compare_hands(hand, table.dealer)
            
        hand.outcome_flag = outcome.flag.value
          
        winnings += actions.handle_payout(hand, outcome)
    
    session['winnings'] = winnings
    session['side_winnings'] = side_winnnigs
    
    table.player.bank.balance += winnings
    table.player.bank.balance += side_winnnigs
    
    session_utils.save_table(table)
    session_utils.save_insurance(insurance)
    
    return redirect(url_for('home'))

def _force_stand_sequence(table: Table):
    has_hands_left = actions.handle_stand(table)
    
    if has_hands_left:
        session_utils.save_table(table)
        return redirect(url_for('home'))
    else:    
        return _end_round_sequence(table)

def _resolve_insurance(table: Table):
    if table.dealer.is_twenty_one:
        actions.dealer_turn(table)
        
        session_utils.save_table(table)
        return _end_round_sequence(table)
    
    outcome = conditions.compare_initial_hands(table)
    
    if outcome.flag != OutcomeFlag.NONE:
        actions.dealer_turn(table)
        
        session_utils.save_table(table)
        return _end_round_sequence(table)
    
    session_utils.save_table(table)
    return redirect(url_for('home'))

@app.route('/')
def home():
    
    # # ===================
    # # FOR DEBUGGING ONLY
    # # ===================
    # create_debug_section(session)
        
    return render_template(
        'index.html', 
        game_active=session.get('game_active', False), 
        current_wager=session.get('current_wager', 0),
        insurance=session_utils.get_insurance(),
        insurance_phase=session.get('insurance_phase', False),
        outcome=session_utils.get_outcome(), 
        table=session_utils.get_table(),  
        winnings=session.get('winnings', 0),
    )

@app.route('/new_game', methods=['POST'])
def new_game():
    session['winnings'] = 0
    session['side_winnings'] = 0
    session['game_active'] = False
    
    session_utils.reset_insurance()
    
    return redirect(url_for('home'))

@app.route('/deal', methods=['POST'])
def deal():    
    table = actions.deal_initial_cards(Table(player=Player()))

    table.player.current_hand.wager += session['current_wager']
    
    outcome = conditions.compare_initial_hands(table)

    session['current_wager'] = 0
    session['game_active'] = True
    session['insurance_phase'] = False
    
    session_utils.reset_insurance()
    
    if conditions.can_take_insurance(table):
        session['insurance_phase'] = True
        
        session_utils.save_table(table)
        session_utils.save_outcome(outcome)
        return redirect(url_for('home'))

    if outcome.flag != OutcomeFlag.NONE:
        actions.dealer_turn(table)
        
        session_utils.save_table(table)
        session_utils.save_outcome(outcome)
        return _end_round_sequence(table)
    
    session_utils.save_table(table)
    session_utils.save_outcome(outcome)
    return redirect(url_for('home'))

@app.route('/hit', methods=['POST'])
@_game_active_required
def hit():
    table = session_utils.get_table()
    
    if table.player.current_hand.value >= 21:
        return _force_stand_sequence(table)
    
    actions.hit_hand(table, table.player.current_hand)

    if table.player.current_hand.value >= 21:
        return _force_stand_sequence(table)
        
    session_utils.save_table(table)
    return redirect(url_for('home'))

@app.route('/double', methods=['POST'])
@_game_active_required
def double_down():
    table = session_utils.get_table()
    
    actions.hit_hand(table, table.player.current_hand)
    table.player.current_hand.wager *= 2
    
    return _force_stand_sequence(table)

@app.route('/split', methods=['POST'])
@_game_active_required
def split():
    table = session_utils.get_table()
    
    if table.player.count() >= 4 or not table.player.current_hand.can_split:
        return redirect(url_for('home'))
    
    actions.split_hand(table)
    next_hand = table.player.hands[table.player.active_hand_index + 1]
    next_hand.wager = table.player.current_hand.wager
    
    session_utils.save_table(table)
    return redirect(url_for('home'))

@app.route('/stand', methods=['POST'])
@_game_active_required
def stand():
    return _force_stand_sequence(session_utils.get_table())

@app.route('/insurance', methods=['POST'])
@_game_active_required
def insurance():
    table = session_utils.get_table()
    insurance = session_utils.get_insurance()
    
    if conditions.can_take_insurance(table):
        actions.update_insurance(table.player.current_hand, insurance)
    
    session['insurance_phase'] = False
    session_utils.save_insurance(insurance)
    
    return _resolve_insurance(table)

@app.route('/decline_insurance', methods=['POST'])
@_game_active_required
def decline_insurance():
    session['insurance_phase'] = False
    return _resolve_insurance(session_utils.get_table())

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

# # ===================
# # FOR DEBUGGING ONLY
# # ===================
# @app.route('/reset')
# def reset():
#     session.clear()
#     return redirect('/')

# def create_debug_section(session):
#     debug_session = dict(session)
        
#     print('== Current Session ==')
#     print(json.dumps(debug_session, indent=4))
    
if __name__ == '__main__':
    app.run(debug=True)
    