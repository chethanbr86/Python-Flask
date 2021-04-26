from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1> Hello Puppy! </h1>"

#2nd example
@app.route('/information')
def info():
    return "<h1> Hello Puppy! you are cute!! </h1>"

@app.route('/puppy/<name>')
def puppypy(name):
    return f"<h1> This is a page for {name.upper()} </h1>"

if __name__ == '__main__':
    app.run()