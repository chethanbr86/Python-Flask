from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecretkey'
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tododata.db'  #'sqlite:///'+os.path.join(basedir, 'todolist.sqlite') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from task_model import views