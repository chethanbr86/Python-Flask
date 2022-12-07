from flask import render_template, redirect, url_for, flash
from task_model import app, db
from task_model.models import Task_list, User
from task_model.forms import RegistrationForm, LoginForm

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
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password_bcrypt=form.password1.data) #password here comes from models (bcrypt)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('todo'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'There was an error with creating a user: {err}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)
