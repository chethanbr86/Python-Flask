from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

# app.config['SECRET_KEY'] = 'mysecretkey'
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db' #'sqlite:///'+os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Task_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    date = db.Column(db.datetime(), nullable=False)
    status = db.Column(db.String(length=10), nullable=False)
    summary = db.Column(db.String(100))

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

if __name__ == '__main__':
    app.run(debug=True)
