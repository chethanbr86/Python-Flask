from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    name = "Chethan"
    letters = list(name)
    pup_dic = {'pup_name':'Sammy'}
    return render_template('basic_variable.html',name=name,letters=letters, pup_dic=pup_dic)

if __name__ == '__main__':
    app.run(debug=True)