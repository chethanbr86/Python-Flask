import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from task_model.todo_viewform.task_views import todo_blueprint
# from task_model.registration.views import 

app.register_blueprint(todo_blueprint)
# app.register_blueprint()

