from flask import render_template
from todo_list_youtube import app
from datetime import datetime

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

#without database
@app.route('/todo')
def todo():
    tasks = [
        {'id':1, 'name':'task1', 'date': datetime.now(), 'status': 1},
        {'id':2, 'name':'task2', 'date': datetime.now(), 'status': 2},
        {'id':3, 'name':'task3', 'date': datetime.now(), 'status': 3}
    ]
    return render_template('todo.html', tasks=tasks)