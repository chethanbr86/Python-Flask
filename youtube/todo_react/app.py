from flask import Flask, render_template, request, redirect, url_for
from form import Todo
#https://www.youtube.com/watch?v=cb1vy1HpVwk&t=1586s

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'

#direct return
# @app.route('/')
# def index():
#     return f'Hello stranger !'

#html return
# @app.route('/')
# def index_html():
#     return render_template('hello.html')

#direct name string
# @app.route('/<name>') #('/<string:name>') or ('/<int:name>')
# def greet_stranger(name):
#     return f'Hello {name}!'

#html name string
# @app.route('/<name>') #dynamic single name here and in html
# def index_html(name):
#     return render_template('hello.html', name = name)

#without methods
# @app.route('/request_method')
# def hello_world():
#     request_method = request.method
#     return render_template('hello_request.html', request_method=request_method)

# #Same as above with methods
# @app.route('/', methods=['GET','POST'])
# def hello_world():
#     request_method = request.method

#     if request.method == 'POST':
#         first_name = request.form['first_name']
#         return redirect(url_for('name', first_name=first_name))
#     return render_template('hello_request.html', request_method=request_method)

# #routing the above
# @app.route('/name/<first_name>') #('/<string:name>') or ('/<int:name>')
# def name(first_name):
#     return f'{first_name}'

@app.route('/todo', methods=['GET'])
def todo():
    todo_form = Todo()
    return render_template('todo.html', form=todo_form)

if __name__ == '__main__':
    app.run(debug=True)