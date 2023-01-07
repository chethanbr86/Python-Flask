from flask import render_template, Blueprint, redirect, url_for
from task_model import app
from task_model import db
from task_model.models import Todo_List
from task_model.todo_viewform.task_form import AddForm, EditForm, DelForm

todo_blueprint = Blueprint('todo_viewform', __name__)

# @todo_blueprint.route('/')
# def home():
#     return render_template('home.html')

@todo_blueprint.route('/', methods=['GET', 'POST'])
def task_add():
    form = AddForm()
    if form.validate_on_submit():
        new_task = Todo_List(form.task_name.data, form.task_status.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('todo_viewform.todo_list', new_task=new_task))
    return render_template('home.html', form=form)

@todo_blueprint.route('/')
def todo_list():
    tasks = Todo_List.query.all()
    return render_template('home.html', tasks=tasks)

@todo_blueprint.route('/', methods=['GET', 'POST'])
def task_delete():
    form = DelForm()
    if form.validate_on_submit():
        del_task = Todo_List.query.get(form.task_name.data)
        db.session.delete(del_task)
        db.session.commit()
        return redirect(url_for('todo_viewform.todo_list', del_task=del_task))
    return render_template('home.html', form=form)

@todo_blueprint.route('/', methods=['GET', 'POST'])
def task_edit():
    form = EditForm()
    if form.validate_on_submit():
        edit_task = Todo_List.query.get(form.task_name.data)
        db.session.update(edit_task)
        db.session.commit()
        return redirect(url_for('todo_viewform.todo_list', edit_task=edit_task))
    return render_template('home.html', form=form)