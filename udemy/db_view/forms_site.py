from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):
    name = StringField('Name of puppy: ')
    # year = RadioField or BooleanField or SelectField - try these
    submit = SubmitField('Add puppy')

class DelForm(FlaskForm):
    id = IntegerField('Id number of puppy to remove: ')
    submit = SubmitField('Remove puppy')