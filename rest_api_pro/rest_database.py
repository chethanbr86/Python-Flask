#Refer flask restful documentation for more examples
import os
from flask import Flask
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myseckey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

api = Api(app)
jwt = JWT(app, authenticate, identity)

#instead of creating models.py we will do it here instead
class Game(db.Model):
    name = db.Column(db.String(80),primary_key=True)

    def __init__(self,name):
        self.name = name

    def json(self):
        return {'name':self.name}

class GameNames(Resource):
    # @jwt_required()
    game = Game.query.filter_by(name=name).first()

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
    @jwt_required() 
    def get(self):
        return {'games':games}

api.add_resource(GameNames,'/gamename/<string:name>')
api.add_resource(AllNames,'/games')

if __name__ == '__main__':
    app.run(debug=True)