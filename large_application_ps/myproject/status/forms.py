from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):
    name = StringField('Status Name: ')
    status_id = IntegerField('Id of Game: ')
    submit = SubmitField("Add status: ")