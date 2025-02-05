#Taking from v92 and MAnager.db from saved onedrive file
import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField, RadioField, SelectField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd
from flask import send_file
from functools import wraps
from flask import abort
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = 'secret_key' #new
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'c_Manager.db') #change to Manager.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect unauthorized users to login page
login_manager.login_message_category = "info"  # Flash message category

migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # Default role is 'user'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == "admin"
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch user from database

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists! Choose another.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

#Database model
class IncomeExpenseManager(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    date = db.Column(db.Date, nullable=False)
    from_bank = db.Column(db.String(10), nullable=True)
    to_bank = db.Column(db.String(10), nullable=True)
    category = db.Column(db.String(20), nullable=False)
    sub_category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # NEW: Link expense to user
    user = db.relationship('User', backref=db.backref('expenses', lazy=True))  # NEW: Relationship

#Flask-wtfforms 
class IncomeExpenseForm(FlaskForm): #change to IncomeExpenseForm
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    from_bank = RadioField('Select - Spent from bank', choices=[('', 'None'), ('hbank', 'HBank'), ('ibank', 'IBank'), ('pbank', 'PBank'), ('sav_inv_bank','SaveInvestBk'), ('purse','Purse')], validators=[Optional()])
    to_bank = RadioField('Select - Received to bank', choices=[('', 'None'), ('hbank', 'HBank'), ('ibank', 'IBank'), ('pbank', 'PBank'), ('sav_inv_bank','SaveInvestBk'), ('purse','Purse')], validators=[Optional()])
    category = SelectField('Category', choices=[('income','Income'),('expense','Expense')], validators=[DataRequired()]) #,('saving','Saving'),('investment','Investment'),('transfer','Transfer')
    sub_category = StringField('Sub-Category', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[DataRequired(), Length(max=100)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add/Edit Expense')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        role = "admin" if User.query.count() == 0 else "user"  # First user is admin
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('index')) #or view_expenses
        else:
            flash("Login failed! Check your email and password.", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@app.route('/export')
@login_required
def export_to_excel():
    try:
        # Fetch all expenses from the database
        expenses = IncomeExpenseManager.query.all()

        # Convert to a list of dictionaries
        data = [{
            "Date": exp.date.strftime('%Y-%m-%d'),
            "From Bank": exp.from_bank if exp.from_bank else "None",
            "To Bank": exp.to_bank if exp.to_bank else "None",
            "Category": exp.category,
            "Sub-Category": exp.sub_category,
            "Description": exp.description,
            "Amount": exp.amount
        } for exp in expenses]

        # Create a Pandas DataFrame
        df = pd.DataFrame(data)

        # Define a proper file path
        file_path = os.path.join(basedir, "expenses.xlsx")

        # Save to an Excel file using 'openpyxl' engine
        df.to_excel(file_path, index=False, engine="openpyxl")

        # Ensure file exists before sending
        if not os.path.exists(file_path):
            flash("Error: File was not created!", "danger")
            return redirect(url_for('view_expenses'))

        # Return file as a download
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        flash(f"Error exporting file: {str(e)}", "danger")
        return redirect(url_for('view_expenses'))

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/add', methods=['GET','POST'])
@login_required
def add_expense():
    form = IncomeExpenseForm()
    # form.handle_conditional_fields()
    if form.validate_on_submit():
        new_expense = IncomeExpenseManager(date=form.date.data, 
                              from_bank=form.from_bank.data if form.from_bank.data else None, 
                              to_bank=form.to_bank.data if form.to_bank.data else None, 
                              category=form.category.data, 
                              sub_category=form.sub_category.data, 
                              description=form.description.data, 
                              amount=form.amount.data,
                              user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()
        flash("Expenses added successfully!", "success")
        return redirect(url_for('view_expenses'))
    return render_template('add_expense.html', form=form)

@app.route('/view')
@login_required
def view_expenses():
    expenses = IncomeExpenseManager.query.filter_by(user_id=current_user.id).order_by(IncomeExpenseManager.date.desc()).all()   
    return render_template('view_expenses.html', expenses=expenses)

@app.route('/delete/<int:id>')
@login_required
def delete_expense(id):
    del_expense = IncomeExpenseManager.query.get_or_404(id)
    if del_expense.user_id != current_user.id:
        flash("You are not authorized to delete this expense!", "danger")
        return redirect(url_for('view_expenses')) 
    db.session.delete(del_expense)
    db.session.commit()
    flash("Expense deleted successfully!", 'success')
    return redirect(url_for('view_expenses'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    edit_expense = IncomeExpenseManager.query.get_or_404(id)
    if edit_expense.user_id != current_user.id:
        flash("You are not authorized to edit this expense!", "danger")
        return redirect(url_for('view_expenses'))  
    form = IncomeExpenseForm(obj=edit_expense)
    if form.validate_on_submit():
        edit_expense.date = form.date.data
        edit_expense.from_bank = form.from_bank.data if form.from_bank.data else None
        edit_expense.to_bank = form.to_bank.data if form.to_bank.data else None
        edit_expense.category = form.category.data
        edit_expense.sub_category = form.sub_category.data
        edit_expense.description = form.description.data
        edit_expense.amount = form.amount.data
        db.session.commit()
        flash("Expense updated successfully!", "success")
        return redirect(url_for('view_expenses'))
    return render_template('edit_expense.html', form=form, edit_expense=edit_expense)

@app.route('/summary')
@login_required
def category_summary():
    # start_date = request.args.get('start_date', datetime.today().replace(day=1).strftime('%Y-%m-%d'))
    # end_date = request.args.get('end_date', datetime.today().strftime('%Y-%m-%d'))
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Convert to datetime objects
    # start_date = datetime.strptime(start_date, '%Y-%m-%d')
    # end_date = datetime.strptime(end_date, '%Y-%m-%d')

    category_summary = db.session.query(IncomeExpenseManager.category, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.user_id == current_user.id).group_by(IncomeExpenseManager.category).all() #.filter(IncomeExpenseManager.date.between(start_date, end_date))
    # exp_sub_category_summary = db.session.query(IncomeExpenseManager.category, IncomeExpenseManager.sub_category, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.category == 'expense', IncomeExpenseManager.date.between(start_date, end_date)).group_by(IncomeExpenseManager.category, IncomeExpenseManager.sub_category).order_by(IncomeExpenseManager.amount.label('total_amount').desc()).all()
    # inc_sub_category_summary = db.session.query(IncomeExpenseManager.category, IncomeExpenseManager.sub_category, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.category == 'income', IncomeExpenseManager.date.between(start_date, end_date)).group_by(IncomeExpenseManager.category, IncomeExpenseManager.sub_category).order_by(IncomeExpenseManager.amount.label('total_amount').desc()).all()

    query = db.session.query(IncomeExpenseManager.date, IncomeExpenseManager.category, IncomeExpenseManager.sub_category, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.user_id == current_user.id).group_by(IncomeExpenseManager.date, IncomeExpenseManager.category, IncomeExpenseManager.sub_category).order_by(IncomeExpenseManager.date.desc())

    if start_date and end_date: 
        query = query.filter(IncomeExpenseManager.date.between(start_date, end_date))

    exp_sub_category_summary = query.filter(IncomeExpenseManager.category == 'expense').all()
    inc_sub_category_summary = query.filter(IncomeExpenseManager.category == 'income').all()

    from_bank_summary = db.session.query(IncomeExpenseManager.from_bank, db.func.sum(IncomeExpenseManager.amount).label('balance')).filter(IncomeExpenseManager.from_bank.isnot(None), IncomeExpenseManager.user_id == current_user.id).group_by(IncomeExpenseManager.from_bank).all() #, IncomeExpenseManager.date.between(start_date, end_date)
    to_bank_summary = db.session.query(IncomeExpenseManager.to_bank, db.func.sum(IncomeExpenseManager.amount).label('balance')).filter(IncomeExpenseManager.to_bank.isnot(None), IncomeExpenseManager.user_id == current_user.id).group_by(IncomeExpenseManager.to_bank).all() #, IncomeExpenseManager.date.between(start_date, end_date)
    # saving_summary = db.session.query(IncomeExpenseManager.sub_category, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.category == 'saving').group_by(IncomeExpenseManager.sub_category).all()
    # invest_summary = db.session.query(IncomeExpenseManager.sub_category, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.category == 'investment').group_by(IncomeExpenseManager.sub_category).all()
    
    #Selected banks
    # List of banks to include
    included_banks = ['hbank', 'ibank', 'pbank']  # Exclude the other two

    # Filter for 'from_bank' total
    select_from_bank_summary = db.session.query(IncomeExpenseManager.from_bank, db.func.sum(IncomeExpenseManager.amount).label('balance')).filter(IncomeExpenseManager.from_bank.isnot(None)).filter(IncomeExpenseManager.from_bank.in_(included_banks), IncomeExpenseManager.user_id == current_user.id).group_by(IncomeExpenseManager.from_bank).all()
    # Filter for 'to_bank' total
    select_to_bank_summary = db.session.query(IncomeExpenseManager.to_bank, db.func.sum(IncomeExpenseManager.amount).label('balance')).filter(IncomeExpenseManager.to_bank.isnot(None)).filter(IncomeExpenseManager.to_bank.in_(included_banks), IncomeExpenseManager.user_id == current_user.id).group_by(IncomeExpenseManager.to_bank).all()

    # Combine the results
    bank_balances = {}
    for bank, balance in from_bank_summary:
        bank_balances[bank] = bank_balances.get(bank, 0) - balance  # removed - above in from_bank_summary and added - here
    for bank, balance in to_bank_summary:
        bank_balances[bank] = bank_balances.get(bank, 0) + balance

    select_bank_balances = {}
    for bank, balance in select_from_bank_summary:
        select_bank_balances[bank] = select_bank_balances.get(bank, 0) - balance  # removed - above in from_bank_summary and added - here
    for bank, balance in select_to_bank_summary:
        select_bank_balances[bank] = select_bank_balances.get(bank, 0) + balance


    # Calculate total balance of all banks
    total_bank_balance = sum(bank_balances.values())

    select_total_bank_balance = sum(select_bank_balances.values())
    
    return render_template('category_summary.html', category_summary=category_summary, exp_sub_category_summary=exp_sub_category_summary, inc_sub_category_summary=inc_sub_category_summary, bank_balances=bank_balances, total_bank_balance=total_bank_balance, select_bank_balances=select_bank_balances, select_total_bank_balance=select_total_bank_balance, start_date=start_date, end_date=end_date) #saving_summary=saving_summary, invest_summary=invest_summary,start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'),

@app.route('/filtersummary')
@login_required
def category_filter():
    categories = ["expense", "income"] #"saving", "investment",
    category_data = {}

    for category in categories:
        sub_categories = db.session.query(IncomeExpenseManager.sub_category).filter(IncomeExpenseManager.category == category, IncomeExpenseManager.user_id == current_user.id).distinct().all()
        sub_categories = [row[0] for row in sub_categories]  # Extract values

        selected_sub_category = request.args.get(f'sub_category_{category}', sub_categories[0] if sub_categories else None)

        sub_cat_des_summary = (db.session.query(IncomeExpenseManager.date, IncomeExpenseManager.sub_category, IncomeExpenseManager.description, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.sub_category == selected_sub_category, IncomeExpenseManager.category == category, IncomeExpenseManager.user_id == current_user.id).group_by(IncomeExpenseManager.date, IncomeExpenseManager.sub_category, IncomeExpenseManager.description).order_by(IncomeExpenseManager.date.desc(), db.func.sum(IncomeExpenseManager.amount).desc()).all())
        
        category_data[category] = {
            "sub_categories": sub_categories,
            "selected_sub_category": selected_sub_category,
            "sub_cat_des_summary": sub_cat_des_summary
        }

    return render_template("category_Filter.html", category_data=category_data)

if __name__ == '__main__':
    # with app.app_context(): #using flask_migrate instead of this to avoid circular import
    #     db.create_all() #To ensure this runs within the application context 
    app.run(debug=True)

#Run in terminal
# flask db init
# flask db migrate -m "Initial migration." or "Added user authentication"
# flask db upgrade