import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#Blueprints have to be registered after db
from myproject.games.views import games_blueprints
from myproject.status.views import status_blueprints

app.register_blueprint(games_blueprints, url_prefix='/games')
app.register_blueprint(status_blueprints, url_prefix='/status')