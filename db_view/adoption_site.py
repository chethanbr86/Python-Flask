from types import MethodDescriptorType
from flask import Flask, render_template, url_for, redirect
import os
from flask.helpers import flash
from forms_site import  AddForm , DelForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

#Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

#Models
class Puppy(db.Model):
    __tablename__ = 'puppies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f'puppy name: {self.name, self.id}'


#view fuctions for forms
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add',methods=['GET','POST'])
def add_pup():
    form = AddForm()

    if form.validate_on_submit():
        #name = form.name.data
        new_pup = Puppy(form.name.data)        

        db.session.add(new_pup)
        db.session.commit()
        return redirect(url_for('list_pup'))
    return render_template('add.html',form=form)

@app.route('/list')
def list_pup():
    puppies = Puppy.query.all()
    return render_template('list.html',puppies=puppies)

@app.route('/delete',methods=['GET','POST'])
def del_pup():
    form = DelForm()

    if form.validate_on_submit():
        #id = form.id.data
        pup = Puppy.query.get(form.id.data)

        # db.session.delete(pup)
        # db.session.commit()
        # return redirect(url_for('list_pup'))

        #This is from another user CM
        if pup:
            flash(f'{pup.name} has been checked out')
        
            db.session.delete(pup)
            db.session.commit()
            return redirect(url_for('list_pup'))
        else:
            flash(f'No pup with id {form.id.data}')
    return render_template('delete.html',form=form)

# There should have been another app route which reroutes to error page when wrong 
# id is selected in delete page.
# Also find a way in list page to show id numbers

#you can follow carles in Q&A

if __name__ == '__main__':
    app.run(debug=True)
