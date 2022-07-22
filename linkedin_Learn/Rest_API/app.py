from email import message
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(message='Hello World!')

# If you want to make custom error page 
@app.route('/not_found')
def not_found():
    return jsonify(message='Page you are looking for is not found'), 404

if __name__=='__main__':
    app.run()