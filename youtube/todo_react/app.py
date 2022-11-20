from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# @app.route('/')
# def index():
#     return f'Hello stranger !'

# @app.route('/')
# def index_html():
#     return render_template('hello.html')

# @app.route('/<name>') #('/<string:name>') or ('/<int:name>')
# def greet_stranger(name):
#     return f'Hello {name}!'

# @app.route('/<name>') #dynamic single name here and in html
# def index_html(name):
#     return render_template('hello.html', name = name)


# @app.route('/request_method')
# def hello_world():
#     request_method = request.method
#     return render_template('hello_request.html', request_method=request_method)


#Same as above with methods
@app.route('/', methods=['GET','POST'])
def hello_world():
    request_method = request.method

    if request.method == 'POST':
        print('-----------------------')
        print(request.form)
        print('-----------------------')
        return redirect(url_for('name'))
    return render_template('hello_request.html', request_method=request_method)
#See how get changes to post as you submit - not working or me

@app.route('/name') #('/<string:name>') or ('/<int:name>')
def name():
    return 'name'

if __name__ == '__main__':
    app.run(debug=True)