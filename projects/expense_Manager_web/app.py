import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

app = Flask(__name__)

app.secret_key = 'secret_key' #new
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'expenses.db') #change to Manager.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#put radio buttons to select if its hbank, ibank, pbank - may be not required, just write a python function to store variables and display balance

#Database model
class Expense(db.Model): #change to ExpenseManager
    id = db.Column(db.Integer, primary_key=True) #how to reset if deleted?
    date = db.Column(db.Date, nullable=False)
    bank = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    sub_category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

#Flask-wtfforms #give dropdown option for categories and sub categories in forms
class ExpenseForm(FlaskForm): #change to IncomeExpenseForm
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    # bank = StringField('Bank', validators=[DataRequired(), Length(max=10)])
    bank = RadioField('Select the bank', choices=[('hbank','HBank'),('ibank','IBank'),('pbank','PBank')])
    # category = StringField('Category', validators=[DataRequired(), Length(max=20)])
    category = SelectField('Select among 4 categories', choices=[('income','Income'),('expense','Expense'),('saving','Saving'),('investment','Investment'),('transfer','Transfer')])
    sub_category = StringField('sub_Category', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[DataRequired(), Length(max=100)])
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
        new_expense = Expense(date=form.date.data, bank=form.bank.data, category=form.category.data, sub_category=form.sub_category.data, description=form.description.data, amount=form.amount.data)
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
    del_expense = Expense.query.get_or_404(id)
    db.session.delete(del_expense)
    db.session.commit()
    flash("Expense deleted successfully!", 'success')
    return redirect(url_for('view_expenses'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    edit_expense = Expense.query.get_or_404(id)
    form = ExpenseForm(obj=edit_expense)
    if form.validate_on_submit():
        edit_expense.date = form.date.data
        edit_expense.bank = form.bank.data
        edit_expense.category = form.category.data
        edit_expense.sub_category = form.sub_category.data
        edit_expense.description = form.description.data
        edit_expense.amount = form.amount.data
        db.session.commit()
        flash("Expense updated successfully!", "success")
        return redirect(url_for('view_expenses'))
    return render_template('edit_expense.html', form=form, edit_expense=edit_expense)

class Banking:
    income_total = 0
    expense_total = 0
    saving_total = 0
    invest_total = 0
    total_balance = 0
    road_to_crore = 1 - total_balance
    hbank_balance = 0
    ibank_balance = 0
    pbank_balance = 0

    @classmethod
    def total_balance():
        pass

    #Also include transfer - which is transfer of funds between banks

if __name__ == '__main__':
    with app.app_context():
        db.create_all() #To ensure this runs within the application context
    app.run(debug=True)