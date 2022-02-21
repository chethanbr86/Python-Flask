from flask import Flask
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myseckey'
api = Api(app)
jwt = JWT(app, authenticate, identity)

games = []

class GameNames(Resource):
    # @jwt_required()
    def get(self,name):
        for game in games:
            if game['name'] == name:
                return game
        return {'name':None}, 404

    def post(self,name):
        game = {'name':name}
        games.append(game)
        return game

    def delete(self,name):
        for ind,game in enumerate(games):
            if game['name'] == name:
                deleted_game = games.pop(ind)
                print(deleted_game)
                return {'note':'delete success'}

class AllNames(Resource):
    @jwt_required() #Because of this we will need authorization like we created before using Flask-login, if names given on website, but here we can use given names, jose and mimi
    #So in postman: POST: http://127.0.0.1:5000/auth
    #better to follow video 122
    def get(self):
        return {'games':games}

api.add_resource(GameNames,'/gamename/<string:name>')
api.add_resource(AllNames,'/games')

if __name__ == '__main__':
    app.run(debug=True)