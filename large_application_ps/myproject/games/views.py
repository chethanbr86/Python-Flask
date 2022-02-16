from flask import Blueprint, render_template, redirect, url_for
from myproject import db
from myproject.models import Playstation
from myproject.games.forms import AddForm, DelForm

games_blueprints = Blueprint('games',__name__, template_folder='templates/games')

@games_blueprints.route('/add', methods=['GET','POST'])
def add():
    form = AddForm()

    if form.validate_on_submit():
        new_game = Playstation(form.name.data) #name from game_forms.py addform
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('games.list'))
    return render_template('add.html', form=form)

@games_blueprints.route('/list') 
def list():
    games = Playstation.query.all()
    return render_template('list.html', games=games)

@games_blueprints.route('/delete', methods=['GET','POST'])
def delete():
    form = DelForm()

    if form.validate_on_submit():
        delete_game = Playstation.query.get(form.id.data)
        db.session.delete(delete_game)
        db.session.commit()
        return redirect(url_for('games.list'))
    return render_template('delete.html', form=form)