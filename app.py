from flask import Flask, render_template, session

app = Flask(__name__)

app.secret_key = 'some_top_secret_key'

@app.route('/')
def home():
    return render_template('index.html')

app.route('/deal')
def exe_init_deal():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    