from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

games = []

class GameNames(Resource):
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
    def get(self):
        return {'games':games}

api.add_resource(GameNames,'/gamename/<string:name>')
api.add_resource(AllNames,'/games')

if __name__ == '__main__':
    app.run(debug=True)