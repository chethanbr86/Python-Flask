from flask import render_template, url_for, flash, redirect, request, Blueprint
from task_model import db
from task_model.models import Todo_List
from task_model.todo_viewform.task_form import AddForm, EditForm, DelForm

todo_blueprint = Blueprint('todo_blueprint', __name__)

@todo_blueprint.route('/')
def home():
    return render_template('home.html')