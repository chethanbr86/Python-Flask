from flask import Blueprint, render_template, redirect, url_for, request

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    # data = request.form
    # print(data)
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return redirect(url_for("views.home"))

@auth.route('/signup', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
    return render_template("sign_up.html")