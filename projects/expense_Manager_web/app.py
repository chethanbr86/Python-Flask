import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from sqlalchemy import Enum
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

app = Flask(__name__)

app.secret_key = 'secret_key' #new
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Manager.db') #change to Manager.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

#Database model
class IncomeExpenseManager(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    date = db.Column(db.Date, nullable=False)
    from_bank = db.Column(Enum('hbank', 'ibank', 'pbank', name='bank_enum'), nullable=False)
    to_bank = db.Column(Enum('hbank', 'ibank', 'pbank', name='bank_enum'), nullable=True)
    category = db.Column(Enum('income', 'expense', 'saving', 'investment', 'transfer', name='category_enum'), nullable=False)
    sub_category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

#Flask-wtfforms 
class IncomeExpenseForm(FlaskForm): #change to IncomeExpenseForm
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    from_bank = RadioField('Select - Spent from bank', choices=[('', ''), ('hbank', 'HBank'), ('ibank', 'IBank'), ('pbank', 'PBank')], validators=[Optional()])
    to_bank = RadioField('Select - Received to bank', choices=[('', ''), ('hbank', 'HBank'), ('ibank', 'IBank'), ('pbank', 'PBank')], validators=[Optional()])
    category = SelectField('Category', choices=[('income','Income'),('expense','Expense'),('saving','Saving'),('investment','Investment'),('transfer','Transfer')], validators=[DataRequired()])
    sub_category = StringField('Sub-Category', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[DataRequired(), Length(max=100)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add/Edit Expense')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET','POST'])
def add_expense():
    form = IncomeExpenseForm()
    # form.handle_conditional_fields()
    if form.validate_on_submit():
        new_expense = IncomeExpenseManager(date=form.date.data, 
                              from_bank=form.from_bank.data, 
                              to_bank=form.to_bank.data, 
                              category=form.category.data, 
                              sub_category=form.sub_category.data, 
                              description=form.description.data, 
                              amount=form.amount.data)
        db.session.add(new_expense)
        db.session.commit()
        flash("Expenses added successfully!", "success")
        return redirect(url_for('view_expenses'))
    return render_template('add_expense.html', form=form)

@app.route('/view')
def view_expenses():
    expenses = IncomeExpenseManager.query.order_by(IncomeExpenseManager.date.desc()).all()
    return render_template('view_expenses.html', expenses=expenses)

@app.route('/delete/<int:id>')
def delete_expense(id):
    del_expense = IncomeExpenseManager.query.get_or_404(id)
    db.session.delete(del_expense)
    db.session.commit()
    flash("Expense deleted successfully!", 'success')
    return redirect(url_for('view_expenses'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    edit_expense = IncomeExpenseManager.query.get_or_404(id)
    print(edit_expense.__dict__)  
    form = IncomeExpenseForm(obj=edit_expense)
    if form.validate_on_submit():
        edit_expense.date = form.date.data
        edit_expense.from_bank = form.from_bank.data
        edit_expense.to_bank = form.to_bank.data
        edit_expense.category = form.category.data
        edit_expense.sub_category = form.sub_category.data
        edit_expense.description = form.description.data
        edit_expense.amount = form.amount.data
        db.session.commit()
        flash("Expense updated successfully!", "success")
        return redirect(url_for('view_expenses'))
    return render_template('edit_expense.html', form=form, edit_expense=edit_expense)

@app.route('/summary')
def category_summary():
    category_summary = db.session.query(IncomeExpenseManager.category, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).group_by(IncomeExpenseManager.category).all()
    sub_category_summary = db.session.query(IncomeExpenseManager.category, IncomeExpenseManager.sub_category, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).group_by(IncomeExpenseManager.category, IncomeExpenseManager.sub_category).order_by(IncomeExpenseManager.amount.label('total_amount').desc()).all()
    from_bank_summary = db.session.query(IncomeExpenseManager.from_bank, db.func.sum(-IncomeExpenseManager.amount).label('balance')).filter(IncomeExpenseManager.from_bank.isnot(None)).group_by(IncomeExpenseManager.from_bank).all()
    to_bank_summary = db.session.query(IncomeExpenseManager.to_bank, db.func.sum(IncomeExpenseManager.amount).label('balance')).filter(IncomeExpenseManager.to_bank.isnot(None)).group_by(IncomeExpenseManager.to_bank).all()
   
    # Combine the results
    bank_balances = {}
    for bank, balance in from_bank_summary:
        bank_balances[bank] = bank_balances.get(bank, 0) + balance 
    for bank, balance in to_bank_summary:
        bank_balances[bank] = bank_balances.get(bank, 0) + balance

    # Calculate total balance of all banks
    total_bank_balance = sum(bank_balances.values())
    
    return render_template('category_summary.html', category_summary=category_summary, sub_category_summary=sub_category_summary, bank_balances=bank_balances, total_bank_balance=total_bank_balance)

if __name__ == '__main__':
    # with app.app_context(): #using flask_migrate instead of this to avoid circular import
    #     db.create_all() #To ensure this runs within the application context 
    app.run(debug=True)

#Run in terminal
# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade

