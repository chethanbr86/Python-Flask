# from task_model import app
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecretkey'
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tododata.db'  #'sqlite:///'+os.path.join(basedir, 'todolist.sqlite') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from datetime import datetime

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(length=15), nullable=False, unique=True)
#     email_address = db.Column(db.String(length=20), nullable=False, unique=True)
#     password_hash = db.Column(db.String(length=60), nullable=False)
#     hours = db.Column(db.Integer(), nullable=False, default=24)

class Task_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(length=10), nullable=False)
    summary = db.Column(db.String(100))

    def __repr__(self):
        return f'Task {self.id, self.name, s}'

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

if __name__ == '__main__':
    app.run(debug=True)
