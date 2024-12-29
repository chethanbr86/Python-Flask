from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
import datetime

app = Flask(__name__)
app.secret_key = 'secret_key' #new
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://expenser_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#put radio buttons to select if its hbank, ibank, pbank

#Database model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)

#Flask-wtfforms
class ExpenseForm(FlaskForm):
    pass