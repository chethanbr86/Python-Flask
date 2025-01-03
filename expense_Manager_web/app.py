import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
import datetime

app = Flask(__name__)

app.secret_key = 'secret_key' #new
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#put radio buttons to select if its hbank, ibank, pbank

#Database model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    sub_category = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)

#Flask-wtfforms
class ExpenseForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired(), Length(max=10)])
    sub_category = StringField('sub_Category', validators=[DataRequired(), Length(max=20)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Expense')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET','POST'])
def add_expense():
    #without forms
    # if request.method == 'POST':
    #     date = request.form['date']
    #     category = request.form['category']
    #     sub_category = request.form['sub_category']
    #     amount = request.form['amount']

    #     if not (date and category and sub_category and amount):
    #         flash('All fields are required!','error')
    #         return redirect(url_for('add_expense'))
        
    #     new_expense = Expense(date=datetime.datetime.strptime(date, '%Y-%m-%d').date(), category = category, sub_category = sub_category, amount = float(amount))
    #     db.session.add(new_expense)
    #     db.session.commit()
    #     flash("Expenses added successfully!", "success")
    #     return redirect(url_for('view_expenses'))
    # return render_template('add_expense.html')

    #with forms
    form = ExpenseForm()
    if form.validate_on_submit():
        new_expense = Expense(date=form.date.data, category=form.category.data, sub_category=form.sub_category.data, amount=form.amount.data)
        db.session.add(new_expense)
        db.session.commit()
        flash("Expenses added successfully!", "success")
        return redirect(url_for('view_expenses'))
    return render_template('add_expense.html', form=form)

@app.route('/view')
def view_expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template('view_expenses.html', expenses=expenses)

@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", 'success')
    return redirect(url_for('view_expenses'))

#Another way of delete
# @my_task_bp.route('/task_delete', methods=['GET','POST'])
# def task_delete():
#     form = DelForm()

#     if form.validate_on_submit():
#         del_task = Mytodo_List.query.get(form.id.data)
#         db.session.delete(del_task)
#         db.session.commit()
#         return redirect(url_for('view_form.task_list', del_task=del_task))
#     return render_template('delete_task.html', form=form)

# @my_task_bp.route('/task_edit', methods=['GET','POST'])
# def task_edit():
#     form = EditForm()

#     if form.validate_on_submit():
#         edit_task = Mytodo_List.query.get(form.id.data)
#         db.session.update(edit_task)
#         db.session.commit()
#         return redirect(url_for('view_form.task_list', edit_task=edit_task))
#     return render_template('delete_task.html', form=form)

#Include a function to edit like above

if __name__ == '__main__':
    with app.app_context():
        db.create_all() #To ensure this runs within the application context
    app.run(debug=True)