from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

# from udemy.db_view.forms_site import DelForm

class Addform(FlaskForm):
    name = StringField('Name of the game: ')
    submit = SubmitField('Add Game')

class DelForm(FlaskForm):
    id = IntegerField('Id number of game to be removed: ')
    submit = SubmitField('Remove game')
