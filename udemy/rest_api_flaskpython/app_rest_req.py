from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'gundu'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
#        for i in items:
#            if i['name'] == name:
#                return i
#another method instead of above commented code
        item = next(filter(lambda x: x['name'] == name, items), None)  #list returns a list of all items matching filter function in this case only one item in a list 
        return {'item': item}, 200 if item is not None else 404        # and hence we can use next which gives the first item found by filter function in this case not in a list
                                                                       # next can give an error if there are no items and hece will have to give None as default value
    def post(self, name):     
        if next(filter(lambda x: x['name'] == name, items), None):
            return {f'message':'An item wih name {name} already exists'}, 400
        data = request.get_json()
        item = {
            'name': name,
            'price':data['price']
        }
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)