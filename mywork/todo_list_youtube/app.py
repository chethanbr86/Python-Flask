from flask import Flask, render_template, redirect, url_for
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/todo')
def todo():
    tasks = [
        {'id':1, 'name':'task1', 'date': datetime.now(), 'status': 1},
        {'id':2, 'name':'task2', 'date': datetime.now(), 'status': 2},
        {'id':3, 'name':'task3', 'date': datetime.now(), 'status': 3}
    ]
    return render_template('todo.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
