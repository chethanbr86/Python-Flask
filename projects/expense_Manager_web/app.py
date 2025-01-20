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

#put radio buttons to select if its hbank, ibank, pbank - may be not required, just write a python function to store variables and display balance

#Database model
class Expense(db.Model): #change to ExpenseManager
    id = db.Column(db.Integer, primary_key=True) #how to reset if deleted?
    date = db.Column(db.Date, nullable=False)
    from_bank = db.Column(db.String(10), nullable=False)
    to_bank = db.Column(db.String(10), nullable=True)
    category = db.Column(db.String(20), nullable=False)
    sub_category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

#Flask-wtfforms #give dropdown option for categories and sub categories in forms
class ExpenseForm(FlaskForm): #change to IncomeExpenseForm
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    # bank = StringField('Bank', validators=[DataRequired(), Length(max=10)])
    from_bank = RadioField('Select the from bank', choices=[('hbank','HBank'),('ibank','IBank'),('pbank','PBank')], validators=[DataRequired()])
    to_bank = RadioField('Select the to bank', choices=[('hbank','HBank'),('ibank','IBank'),('pbank','PBank')], coerce=str)
    # category = StringField('Category', validators=[DataRequired(), Length(max=20)])
    category = SelectField('Category', choices=[('income','Income'),('expense','Expense'),('saving','Saving'),('investment','Investment'),('transfer','Transfer')], validators=[DataRequired()])
    sub_category = StringField('Sub-Category', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[DataRequired(), Length(max=100)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add/Edit Expense')

    # Method to handle conditional logic for 'to_bank' visibility
    def handle_conditional_fields(self):
        if self.category.data != 'transfer':  # If the category is not 'transfer', disable 'to_bank'
            self.to_bank.render_kw = {'disabled': True}
            self.to_bank.data = None  # Optionally clear the value

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
    form.handle_conditional_fields()
    if form.validate_on_submit():
        if form.category.data == "transfer" and not form.to_bank.data:
            flash("You must select a 'To Bank' for transfers.", "error")
            return render_template('add_expense.html', form=form)
        new_expense = Expense(date=form.date.data, 
                              from_bank=form.from_bank.data if form.category.data == "transfer" else None, 
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
    return render_template('add_expense.html', form=form, edit_expense=edit_expense)

# class Banking:
#     income_total = 0
#     expense_total = 0
#     saving_total = 0
#     invest_total = 0
#     total_balance = 0
#     road_to_crore = 1 - total_balance
#     hbank_balance = 0
#     ibank_balance = 0
#     pbank_balance = 0

#     @classmethod
#     def total_balance():
#         pass

#     #Also include transfer - which is transfer of funds between banks

@app.route('/summary')
def category_summary():
    category_summary = db.session.query(Expense.category, db.func.sum(Expense.amount).label('total_amount')).group_by(Expense.category).all()
    sub_category_summary = db.session.query(Expense.category, Expense.sub_category, db.func.sum(Expense.amount).label('total_amount')).group_by(Expense.category, Expense.sub_category).all()
    return render_template('category_summary.html', category_summary=category_summary, sub_category_summary=sub_category_summary)

# @app.route('/summary')
# def sub_category_summary():
#     sub_summary = db.session.query(Expense.sub_category, func.sum(Expense.amount).label('total_amount')).group_by(Expense.sub_category).all()
#     return render_template('category_summary.html', sub_summary=sub_summary)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() #To ensure this runs within the application context
    app.run(debug=True)