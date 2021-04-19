from types import MethodDescriptorType
from flask import Flask, render_template, url_for, redirect
import os
from flask.helpers import flash
from ex10_forms import  AddForm , DelForm, OwnerForm
# from ex10_relation import rel_own, owner_puppy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mskey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

class puppy_adopt(db.Model):
    __tablename__ = 'puppy_names'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    owner = db.relationship('owner_puppy',backref='puppy',uselist=False)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f'Puppy name is {self.name}, id is {self.id} and owner is {self.owner.name}'
        else:
            return f'Puppy name is {self.name} and id is {self.id} and has no owner yet!'

class owner_puppy(db.Model):
    __tablename__ = 'owner_names'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppy_names.id'))

    def __init__(self,name,puppy_id):
        self.name = name
        self.puppy_id = puppy_id

    def __repr__(self):        
        return f'owner is {self.name}'

@app.route('/')
def index():
    return render_template('ex10_home.html')

@app.route('/add',methods=['GET','POST'])
def add_pup():
    form = AddForm()

    if form.validate_on_submit():
        #name = form.name.data
        new_pup = puppy_adopt(form.name.data)        

        db.session.add(new_pup)
        db.session.commit()
        return redirect(url_for('list_pup'))
    return render_template('ex10_add.html',form=form)

@app.route('/list')
def list_pup():
    puppies = puppy_adopt.query.all()
    return render_template('ex10_list.html',puppies=puppies)

@app.route('/delete',methods=['GET','POST'])
def del_pup():
    form = DelForm()

    if form.validate_on_submit():
        #id = form.id.data
        pup = puppy_adopt.query.get(form.id.data)
        if pup:
            flash(f'{pup.name} has been checked out')
        
            db.session.delete(pup)
            db.session.commit()
            return redirect(url_for('list_pup'))
        else:
            flash(f'No pup with id {form.id.data}')
    return render_template('ex10_delete.html',form=form)

@app.route('/owner',methods=['GET','POST'])
def own_pup():
    form = OwnerForm()

    if form.validate_on_submit():
        
        #name = form.name.data
        puppy_id = form.pup_id.data 
        new_owner = owner_puppy(form.name.data, puppy_id)     

        db.session.add(new_owner)
        db.session.commit()
        return redirect(url_for('list_pup'))
    return render_template('ex10_owner.html',form=form)

# @app.route('/owner',methods=['GET','POST'])
# def own_pup():
#     form = OwnerForm()

#     if form.validate_on_submit():
        
#         if puppy_adopt(form.name.data) is not '':
#             puppy_id = form.pup_id.data 
#             new_owner = owner_puppy(form.name.data, puppy_id)     

#             db.session.add(new_owner)
#             db.session.commit()
#             return redirect(url_for('list_pup'))
#         else:
#             flash(f'No pup with id to add owner!')
#     return render_template('ex10_owner.html',form=form)

    #Here there is a bug, where owner name can be added for puppy id which is still not in database

if __name__ == '__main__':
    app.run(debug=True)
