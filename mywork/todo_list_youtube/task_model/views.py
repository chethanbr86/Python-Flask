from flask import render_template
from task_model import app
from task_model.models import Task_list
from datetime import datetime

#without database
@app.route('/todo')
def todo():
    tasks = [
        {'id':1, 'name':'task1', 'date': datetime.now(), 'status': 1},
        {'id':2, 'name':'task2', 'date': datetime.now(), 'status': 2},
        {'id':3, 'name':'task3', 'date': datetime.now(), 'status': 3}
    ]
    return render_template('todo.html', tasks=tasks)