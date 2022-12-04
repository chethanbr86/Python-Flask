from flask import render_template, redirect, url_for
from task_model import app
from task_model.models import Task_list, User
from task_model.forms import RegistrationForm
from task_model import db

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

@app.route('/register_page', methods=['GET','POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('todo'))
    return render_template('register.html', form=form)
