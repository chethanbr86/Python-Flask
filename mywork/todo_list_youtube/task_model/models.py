from task_model import db
from datetime import datetime

class Task_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    # date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(length=10), nullable=False)
    summary = db.Column(db.String(100))

    def __repr__(self):
        return f'Task {self.id, self.name}'