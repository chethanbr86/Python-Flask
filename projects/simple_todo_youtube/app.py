from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '9e3f1a08c9572411d3c88464'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  #'sqlite:///tododata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    # def __repr__(self):
    #     return f'Task {self.id, self.name, self.date, self.status}'

@app.route('/')
def home():
    task_list = Task_list.query.all()
    return render_template('home.html', task_list=task_list)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    new_task = Task_list(name=name, status=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<int:id>')
def update(id):
    todo = Task_list.query.get(id)
    todo.status = not todo.status  #why this line
    # db.session.update(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Task_list.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)