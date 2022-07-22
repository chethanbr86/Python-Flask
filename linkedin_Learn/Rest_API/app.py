from email import message
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(message='Hello World!')

# If you want to make custom error page 
@app.route('/not_found')
def not_found():
    return jsonify(message='Page you are looking for is not found'), 404

@app.route('/parameters')
def parameters():
    name = request.args.get('name')  #request is not required below since we are giving arguments in path as well as function
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message='Sorry '+name+', you are too young!'), 401
    else:
        return jsonify(message='Welcome '+name+', you are old enough.')

@app.route('/url_params/<string:name>/<int:age>') #here string specification is from flask
def url_params(name:str, age:int): #here string specification in from python
    if age < 18:
        return jsonify(message='Sorry '+name+', you are too young!'), 401
    else:
        return jsonify(message='Welcome '+name+', you are old enough.')
        #Here in postman, no need to enter in query parameters like above function, but only in url

if __name__=='__main__':
    app.run(debug=True)