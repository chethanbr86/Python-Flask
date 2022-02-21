from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

# from udemy.db_view.forms_site import DelForm

class AddForm(FlaskForm):
    name = StringField('Name of the game: ')
    submit = SubmitField('Add Game')

class DelForm(FlaskForm):
    id = IntegerField('Id number of game to be removed: ')
    submit = SubmitField('Remove game')

class AddStatusForm(FlaskForm):
    name = StringField('Status Name: ')
    status_id = IntegerField('Id of Game: ')
    submit = SubmitField("Add status: ")

#also add class for how much money you have bought if bought and add up the money
