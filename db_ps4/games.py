import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import AddForm, DelForm
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

#SQL section
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#Modelling section
class Playstation(db.Model):
    __tablename__ = 'games_played'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'game name: {self.id, self.name}'

#View functions
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=['GET','POST'])
def add_game():
    form = AddForm()

    if form.validate_on_submit():
        new_game = Playstation(form.name.data) #name from form.py addform
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('list_game'))
    return render_template('add.html', form=form)

@app.route('/list')
def list_game():
    games = Playstation.query.all()
    return render_template('list.html', games=games)

@app.route('/delete', methods=['GET','POST'])
def del_game():
    form = DelForm()

    if form.validate_on_submit():
        delete_game = Playstation(form.id.data) #refer to adoption_site.py for small change here with if statement
        #another way being showing error page like below@app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
        db.session.delete(delete_game)
        db.session.commit()
        return redirect(url_for('list_game'))
    return render_template('delete.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)