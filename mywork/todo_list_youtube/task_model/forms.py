from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField

class RegistrationForm(FlaskForm):
    username = StringField(label='User Name: ')
    email_address = StringField(label='Email Address: ')
    password1 = PasswordField(label='Password: ')
    password2 = PasswordField(label='Confirm Password: ')
    sumbit = SubmitField(label='Create Account')


