from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        for i in items:
            if i['name'] == name:
                return i
        return {'item':None}, 404

    def post(self, name):     
        item = {
            'name':name,
            'price':11.00
        }
        items.append(item)
        return item, 201

api.add_resource(Item,'/item/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)