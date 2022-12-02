from flask import render_template
from task_model import app
from task_model.models import Task_list
from datetime import datetime
from task_model.forms import RegistrationForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/todo')
def todo():
    # tasks = [
    #     {'id':1, 'name':'task1',  'status': 1}, #'date': datetime.now(),
    #     {'id':2, 'name':'task2',  'status': 2},
    #     {'id':3, 'name':'task3',  'status': 3}
    # ]
    # return render_template('todo.html', tasks=tasks)
    tasks = Task_list.query.all()
    return render_template('todo.html', tasks=tasks)

@app.route('/register_page')
def register_page():
    form = RegistrationForm()
    return render_template('register.html', form=form)
