# from crypt import methods
from email import message
from enum import unique
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
# The process of converting object into textual representation is called serialization. This is used to serialize a collection of sqlalchemy datarows.
from flask_marshmallow import Marshmallow
import os
#For login and user registration in normal methods, there are Flask-Login, Flask-User
#For API projects, login and others can be managed from JWT
from flask_jwt_extended import JWTManager, jwt_required, create_access_token #This whole line is for login (not registration)

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'supersecret'

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# The below 2 functions are same as we do in views, add and delete
@app.cli.command('db_create')
def db_create():
    db.create_all() #db.create_all and db.drop_all methods are coming from sqlalchemy
    print('Database created!')

@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury', planet_type='Class D', home_star = 'Sol', mass = 3.258e23, radius = 1516, distance = 35.98e6)
    venus = Planet(planet_name='Venus', planet_type='Class K', home_star = 'Sol', mass = 4.867e24, radius = 3760, distance = 67.24e6)
    earth = Planet(planet_name='Earth', planet_type='Class M', home_star = 'Sol', mass = 5.972e24, radius = 3959, distance = 92.96e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='William', last_name='Herschel', email='test@test.com',password='password')
    db.session.add(test_user)
    db.session.commit()
    print('Database seeded!')

#Here we need to create database entries since we are not using html or forms to do it in fronted
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database Destroyed!')


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

#Let's create a function which only responds to GET but not POST
@app.route('/planets', methods=['GET'])
def planets():
    planet_list = Planet.query.all()
    # return jsonify(data=[planet_list]) #This method won't work #we get this error #TypeError: Object of type Planet is not JSON serializable. This is not a problem with html and all, for restapi we are not using html but only flask and hence postman and jsonify
    #Deserialize with marshmallow
    result = planets_schema.dump(planet_list)
    return jsonify(result)

#For registration
@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully.'), 201

@app.route('/login', methods=['POST'])  #Here we should use get but instructor insisted post method
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        #we need to send jwt web toket
        access_token = create_access_token(identity=email)
        return jsonify(message='Login Succeeded!', access_token=access_token)
    else:
        return jsonify(message='Email or password not correct'), 401
# While testing in postman, we can use either form or json type

# Database
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass= Column(Float)
    radius = Column(Float)
    distance = Column(Float)

# For marshmallow
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','first_name','last_name','email','password')

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id','planet_name','planet_type','home_star','mass','radius','distance')

#Instatiating
user_schema = UserSchema() #one record
users_schema = UserSchema(many=True) #collection of records
planet_schema = PlanetSchema
planets_schema = PlanetSchema(many=True)


if __name__=='__main__':
    app.run(debug=True)