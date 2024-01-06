from flask import Flask, render_template, redirect, url_for, Blueprint, flash
from task_model import app
from task_model import db
from task_model.models import Mytodo_List
from task_model.view_form.forms import AddForm, DelForm, EditForm

my_task_bp = Blueprint('view_form',__name__)

@my_task_bp.route('/')
def index():
    return render_template('index.html')

@my_task_bp.route('/task_add', methods=['GET','POST'])
def task_add():
    form = AddForm()

    if form.validate_on_submit():
        new_task = Mytodo_List(form.task_name.data, form.task_status.data)
        db.session.add(new_task) 
        db.session.commit()
        flash(f'Task: {new_task} added') #not working
        return redirect(url_for('view_form.task_list', new_task=new_task))
    return render_template('add_task.html', form=form)

@my_task_bp.route('/task_list')
def task_list():
    tasks = Mytodo_List.query.all()
    return render_template('list_task.html', tasks=tasks)

@my_task_bp.route('/task_delete', methods=['GET','POST'])
def task_delete():
    form = DelForm()

    if form.validate_on_submit():
        del_task = Mytodo_List.query.get(form.id.data)
        db.session.delete(del_task)
        db.session.commit()
        return redirect(url_for('view_form.task_list', del_task=del_task))
    return render_template('delete_task.html', form=form)

@my_task_bp.route('/task_edit', methods=['GET','POST'])
def task_edit():
    form = EditForm()

    if form.validate_on_submit():
        edit_task = Mytodo_List.query.get(form.id.data)
        db.session.update(edit_task)
        db.session.commit()
        return redirect(url_for('view_form.task_list', edit_task=edit_task))
    return render_template('delete_task.html', form=form)