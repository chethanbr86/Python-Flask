import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

app = Flask(__name__)

app.secret_key = 'secret_key' #new
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'expenses.db') #change to Manager.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Database model
class Expense(db.Model): #change to ExpenseManager
    id = db.Column(db.Integer, primary_key=True) #how to sort when some id is deleted
    date = db.Column(db.Date, nullable=False)
    from_bank = db.Column(db.String(10), nullable=False)
    to_bank = db.Column(db.String(10), nullable=True)
    category = db.Column(db.String(20), nullable=False)
    sub_category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

#Flask-wtfforms 
class ExpenseForm(FlaskForm): #change to IncomeExpenseForm
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    from_bank = RadioField('Select - Spent from bank', choices=[('hbank','HBank'),('ibank','IBank'),('pbank','PBank')], validators=[DataRequired()])
    to_bank = SelectField('Select - Received to bank', choices=[('notBank','NotBank'),('hbank','HBank'),('ibank','IBank'),('pbank','PBank')], default='none')
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
    form = ExpenseForm()
    # form.handle_conditional_fields()
    if form.validate_on_submit():
        new_expense = Expense(date=form.date.data, 
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
    print(edit_expense.__dict__)  
    form = ExpenseForm(obj=edit_expense)
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
    from_bank_summary = db.session.query(Expense.from_bank, db.func.sum(Expense.amount).label('total_amount')).group_by(Expense.from_bank).all()
    to_bank_summary = db.session.query(Expense.from_bank, Expense.to_bank, db.func.sum(Expense.amount).label('total_amount')).group_by(Expense.from_bank, Expense.to_bank).all()
    category_summary = db.session.query(Expense.from_bank, Expense.to_bank, Expense.category, db.func.sum(Expense.amount).label('total_amount')).group_by(Expense.from_bank, Expense.to_bank, Expense.category).all()
    sub_category_summary = db.session.query(Expense.from_bank, Expense.to_bank, Expense.category, Expense.sub_category, db.func.sum(Expense.amount).label('total_amount')).group_by(Expense.from_bank, Expense.to_bank, Expense.category, Expense.sub_category).all()
    return render_template('category_summary.html', from_bank_summary=from_bank_summary, to_bank_summary=to_bank_summary, category_summary=category_summary, sub_category_summary=sub_category_summary)

@app.route('/balances')
def view_balances():
    # Get all transactions for from_bank
    from_bank_summary = db.session.query(
        Expense.from_bank, db.func.sum(-Expense.amount).label('balance')
    ).group_by(Expense.from_bank).all()
    
    # Get all transactions for to_bank
    to_bank_summary = db.session.query(
        Expense.to_bank, db.func.sum(Expense.amount).label('balance')
    ).filter(Expense.to_bank.isnot(None)).group_by(Expense.to_bank).all()
    
    # Combine the results
    bank_balances = {}
    for bank, balance in from_bank_summary:
        bank_balances[bank] = bank_balances.get(bank, 0) + balance
    for bank, balance in to_bank_summary:
        bank_balances[bank] = bank_balances.get(bank, 0) + balance
    
    return render_template('view_balances.html', bank_balances=bank_balances)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() #To ensure this runs within the application context
    app.run(debug=True)

