from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, RadioField, SelectField,  
                        TextAreaField, SubmitField)
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykey'

class InfoForm(FlaskForm):
    breed = StringField("What Breed are you?", validators=[DataRequired()]) 
    neutered = BooleanField("Have your puppy been neutered?")
    mood = RadioField('Please choose your mood:', choices=[('Happy','Happy'),('Excited','Excited')])
    food_choice = SelectField(u'Pick your favourite food:', choices=[('Chicken','Chicken'),('BEEF','BEEF'),('Fish','Fish')])
    feedback = TextAreaField()
    submit = SubmitField("Submit")

@app.route('/', methods=['GET','POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session['breed'] = form.breed.data
        session['neutered'] = form.neutered.data
        session['mood'] = form.mood.data
        session['food'] = form.food_choice.data
        session['feedback'] = form.feedback.data

        return redirect(url_for('thank_you')) # this return is for if statement upon submission #without using template file we can directly redirect from here
    return render_template('field1_index.html', form=form) #this return is for whole function

@app.route('/thank_you')
def thank_you():
    return render_template('field1_thank.html')

if __name__ == '__main__':
    app.run(debug=True)
