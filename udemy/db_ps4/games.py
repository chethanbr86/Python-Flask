import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from game_forms import AddForm, DelForm
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

#SQL section
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#Modelling section
class Playstation(db.Model):
    __tablename__ = 'games_played'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    #below line is for creating relation between below class
    game_stat = db.relationship('Game_Status',backref='game',uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.game_stat:
            return f'Game id is : {self.id}, game name is {self.name} and status is {self.game_stat.name}'
        else:
            return f'Game id is : {self.id}, game name is {self.name} and status is None yet!'

#This class has been added to add another status
class Game_Status(db.Model):
    __tablename__ = 'status_games'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    stat_id = db.Column(db.Integer, db.ForeignKey('games_played.id'))

    def __init__(self,name,stat_id):
        self.name = name
        self.stat_id = stat_id

    def __repr__(self):        
        return f'status is {self.stat_id, self.name}'

#View functions
@app.route('/')
def index():
    return render_template('home.html')

#This is for status
@app.route('/add_status', methods=['GET','POST'])
def add_status():
    form = 

@app.route('/add', methods=['GET','POST'])
def add_game():
    form = AddForm()

    if form.validate_on_submit():
        new_game = Playstation(form.name.data) #name from game_forms.py addform
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
        delete_game = Playstation.query.get(form.id.data) #refer to adoption_site.py for small change here with if statement
        #another way being showing error page like below
# def page_not_found(e):
#     return render_template('404.html'), 404
        db.session.delete(delete_game)
        db.session.commit()
        return redirect(url_for('list_game'))
    return render_template('delete.html', form=form)

#Add a function update list like add and delete
#And also try separate list like bought and psplus and free
#Also add a function where you delete invalid id, it will show a flash message

#Above 3 can be done in a project, here next instead of adding owner let's add whether game is free or bought or psplus

if __name__ == '__main__':
    app.run(debug=True)