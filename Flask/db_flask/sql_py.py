import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class puppy(db.Model):

    #Manual table name choice
    __tablename__ = 'puppies' #no need to give table name, it will be auto created

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    age = db.Column(db.Integer)

    def __init__(self,name,age):  #no need to include id, it will be auto created
        self.name = name 
        self.age = age

    # def __repr__(self) -> str:
    #     return super().__repr__()

    def __repr__(self):
        return f'Puppy {self.name} is {self.age} year/s old'

    



