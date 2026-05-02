from functools import wraps

from flask import Flask, render_template, redirect, session

app = Flask(__name__)

app.secret_key = 'some_top_secret_key'

def _game_active_required(func):
    @wraps(func)
    def _game_active_bouncer(*args, **kwargs):
        if not session.get('game_active'):
            return redirect('/')
        
        return func(*args, **kwargs)
    
    return _game_active_bouncer

@app.route('/')
def home():
    is_active = session.get('game_active', False)
    return render_template('index.html', game_active=is_active)

@app.route('/deal', methods=['POST'])
def deal():
    session['game_active'] = True
    return render_template('index.html', game_active=True)

@app.route('/hit', methods=['POST'])
@_game_active_required
def hit():
    return 'SUCCESS, the HIT button works.'

@app.route('/stand', methods=['POST'])
@_game_active_required
def stand():
    return 'SUCCESS, the STAND button works.'

# FOR DEBUGGING PURPOSES
@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)
    