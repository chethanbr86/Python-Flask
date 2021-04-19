from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):
    name = StringField('Name of puppy: ')
    submit = SubmitField('Add puppy')

class DelForm(FlaskForm):
    id = IntegerField('Id number of puppy to remove: ')
    submit = SubmitField('Remove puppy')

class OwnerForm(FlaskForm):
    name = StringField('Name of the owner: ')
    pup_id = IntegerField("Id of Puppy: ")
    submit = SubmitField('Add owner')