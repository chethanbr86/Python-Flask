from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField

class AddForm(FlaskForm):
    task_name = StringField('Name of the task = ')
    task_status = SelectField('Programming Language', choices=[('Not Started','Not Started'), ('In Progress','In Progress'), ('Completed','Completed')])
    submit = SubmitField('Add Task')

class DelForm(FlaskForm):
    id = IntegerField('ID of the task to be removed = ')    
    submit = SubmitField('Delete Task')

class EditForm(FlaskForm):
    id = IntegerField('ID of the task to be edited = ')
    task_status = SelectField('Programming Language', choices=[('Not Started','Not Started'), ('In Progress','In Progress'), ('Completed','Completed')])
    submit = SubmitField('Edit Task')