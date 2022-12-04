from task_model import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=15), nullable=False, unique=True)
    email_address = db.Column(db.String(length=20), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    hours = db.Column(db.Integer(), nullable=False, default=24)
    tasks = db.relationship('Task_list', backref='owned_user', lazy=True)

    # def __repr__(self):
    #     return f'User {self.id, self.username, self.email_address}'

class Task_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(length=10), nullable=False)
    summary = db.Column(db.String(100))
    owner = db.Column(db.Integer(), db.ForeignKey(User.username))

    def __repr__(self):
        return f'Task {self.id, self.name, self.date}'