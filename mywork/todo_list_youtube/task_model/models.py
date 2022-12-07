from task_model import db, login_manager
from datetime import datetime
from task_model import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=15), nullable=False, unique=True)
    email_address = db.Column(db.String(length=20), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    hours = db.Column(db.Integer(), nullable=False, default=24)
    tasks = db.relationship('Task_list', backref='owned_user', lazy=True)

    #if there is budget instead of hours
    # @property
    # def prettier_budget(self):
    #     if len(str(self.budget)) <= 4:
    #         return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
    #     else:
    #         return f'{self.budget}'

    @property
    def password_bcrypt(self):
        return self.password_bcrypt

    @password_bcrypt.setter
    def password_bcrypt(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        
class Task_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(length=10), nullable=False)
    summary = db.Column(db.String(100))
    owner = db.Column(db.Integer(), db.ForeignKey(User.username))

    def __repr__(self):
        return f'Task {self.id, self.name, self.date}'