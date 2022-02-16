from flask import Blueprint, render_template, redirect, url_for
from myproject import db
from myproject.models import Game_Status
from myproject.status.forms import AddForm

status_blueprints = Blueprint('status',__name__, template_folder='templates/status')

@status_blueprints.route('/add', methods=['GET','POST'])
def add():
    form = AddForm()

    if form.validate_on_submit():
        new_Status = Game_Status(form.name.data,form.status_id.data)
        db.session.add(new_Status)
        db.session.commit()
        return redirect(url_for('games.list'))
    return render_template('stat_add.html', form=form)
