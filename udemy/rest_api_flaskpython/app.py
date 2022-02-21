#Storing data in website
from flask import Flask, request, render_template

app = Flask(__name__)

stores = [
    {
        "name":"My store",
        "items": [
            {
                "name":"My item1",
                "price":99.99
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')
#json cannot be a list, has to be dictonary
#json always uses double quotes and not single quotes

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return new_store

@app.route('/store/<string:name>')
def get_store(name):
    #iterate over stores and return if matches else return error message
    for i in stores:
        if i['name'] == name:
            return i
    return {'message':'store not found'}

@app.route('/store')
def get_stores():
    return {'stores':stores} #return jsonify({'stores':stores}) #getting same result without using jsonify
#Since json should be a dictonary but above stores is a list, we are converting it to dictonary in the above line

@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for i in stores:
        if i['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            i['items'].append(new_item)
            return new_item
    return {'message': 'store not found'}

@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for i in stores:
        if i['name'] == name:
            return {'items':i['items']}
    return {'message': 'store not found'}

#As and when you add new store and new item it gets added to new created list but once server is run once again, everything is lost 
# and gets set to default and hence database is used

if __name__ == '__main__':
    app.run()