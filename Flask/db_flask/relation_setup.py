from relationship import db,puppy1,Owner,Toy

#Creating 2 puppies
rufus = puppy1('Rufus')
fido = puppy1('Fido')

# Add puppies to db
db.session.add_all([rufus,fido])
db.session.commit()

# Check!
print(puppy1.query.all())

rufus = puppy1.query.filter_by(name='Rufus').first() #or .all()[0]
print(rufus)

#Creating owner
chetu = Owner('Chethan',rufus.id)

#Giving toys
toy1 = Toy('chew toy',rufus.id)
toy2 = Toy('ball',rufus.id)

db.session.add_all([chetu,toy1,toy2])
db.session.commit()

# Lets grab rufus again
rufus = puppy1.query.filter_by(name='Rufus').first()
print(rufus)

rufus.report_toys()

