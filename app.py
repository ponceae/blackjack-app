from functools import wraps

from flask import Flask, redirect, render_template, session, url_for
import json

from engine import actions, conditions, payouts
from entities import Card, OutcomeFlag, Player, Table
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

def _force_stand_sequence(table: Table):
    has_hands_left = actions.handle_stand(table)
    
    if has_hands_left:
        session_utils.save_table(table)
        return redirect(url_for('home'))
    else:    
        return _end_round_sequence(table)

def _end_round_sequence(table: Table):    
    winnings = 0
    
    for hand in table.player.hands:
        outcome = conditions.compare_hands(hand, table.dealer)
        hand.outcome_flag = outcome.flag.value
        winnings += actions.handle_payout(table.player.current_hand, outcome)
    
    session['winnings'] = winnings
    
    table.player.bank.balance += winnings
    
    session_utils.save_table(table)
    
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

    table.dealer.cards[1] = Card('Spades', 'Ace')

    _wager = session['current_wager']
    table.player.current_hand.wager += _wager
    
    outcome = conditions.compare_initial_hands(table)

    if outcome.flag != OutcomeFlag.NONE:
        actions.dealer_turn(table)
        return _end_round_sequence(table)

    session['current_wager'] = 0
    session['game_active'] = True
    
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

@app.route('/insurance', methods=['POST'])
@_game_active_required
def insurance():
    table = session_utils.get_table()
    
    if conditions.can_take_insurance(table):
        table.player.current_hand.insurance_wager = payouts.get_insurance_cost(
            table.player.current_hand
        )
    
    session_utils.save_table(table)
    return redirect(url_for('home'))

@app.route('/split', methods=['POST'])
@_game_active_required
def split():
    table = session_utils.get_table()
    
    if table.player.count() >= 4 or not table.player.current_hand.can_split:
        return redirect(url_for('home'))
    
    actions.split_hand(table)
    table.player.hands[table.player.active_hand_index + 1].wager = table.player.current_hand.wager
    
    session_utils.save_table(table)
    return redirect(url_for('home'))

@app.route('/stand', methods=['POST'])
@_game_active_required
def stand():
    table = session_utils.get_table()
    
    has_hands_left = actions.handle_stand(table)
    
    if has_hands_left:
        session_utils.save_table(table)
        return redirect(url_for('home'))
    else:
        return _end_round_sequence(table)

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
    