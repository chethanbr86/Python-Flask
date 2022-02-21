from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Student(Resource):
    #def home(self):
        #return 'Hi, how are you, go to next page!'

    def get(self, name):
        return {'student':name}

#api.add_resource(Student,'/')
api.add_resource(Student,'/student/<string:name>')

if __name__ == '__main__':
    app.run()