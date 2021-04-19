from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1> Welcome to the Puppy sale page! Go to /puppy_latin/name to see ur puppy's name in latin! </h1>"

@app.route('/puppy_latin/<name>')
def puppylatin(name):
    for word in name:
        puppylatinname = ''
        if name[-1] == 'y':
            puppylatinname = name[:-1] + 'iful'
        elif name[-1] != 'y':
            puppylatinname = name + 'y'
        return f"<h1> Your puppy latin name is: {puppylatinname} </h1>"

if __name__ == '__main__':
    app.run(debug=True)



