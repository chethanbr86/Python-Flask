from task_model import db
from datetime import datetime

# class User

class Todo_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(length=30), nullable=False, unique=True)
    # task_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    task_date = db.Column(db.DateTime())
    task_status = db.Column(db.String(length=10), nullable=False)
    # task_summary = db.Column(db.Text(100))

    def __init__(self, task_name, task_status, task_date=None):
        self.title = task_name
        self.text = task_status
        if task_date is None:
            self.created_time = datetime.utcnow()
        else:
            self.created_time = task_date

    # def __repr__(self):
    #     return f'Task = {self.task_name, self.task_date, self.task_status}'    