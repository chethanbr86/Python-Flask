from flask import Flask, render_template

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     # return 'Hello World'
#     return '<h1>Hello World</h1>'

# @app.route('/about')
# def about_page1():
#     return '<h1>This page is about </h1>'

# @app.route('/about/<username>')
# def about_page2(username):
#     return f'<h1>This page is about {username}!</h1>'

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    return render_template('market.html')