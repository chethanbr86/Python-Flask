import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
#Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'gamedata.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#Login
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

from socialproject.core.views import core
from socialproject.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(error_pages)