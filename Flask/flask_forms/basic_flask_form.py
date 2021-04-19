from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    breed = StringField("What Breed are you?") 
    # breed is an attribute above
    submit = SubmitField("Submit")

@app.route('/', methods=['GET','POST'])
def index():
    breed = False
    # breed is a variable here
    form = InfoForm()

    if form.validate_on_submit():
        breed = form.breed.data
        # here breed after '=' in above line is the attribute one
        form.breed.data = ''
    return render_template('index_flask_form.html', form=form, breed=breed)

if __name__ == '__main__':
    app.run(debug=True)