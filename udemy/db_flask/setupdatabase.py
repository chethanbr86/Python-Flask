from sql_py import db, puppy

# Creates all the tables
db.create_all()

sam = puppy('Sammy',3)
frank = puppy('Frankie',4)

# Following lines will be none since its not added to database
print(sam.id)
print(frank.id)

# Adding to database
db.session.add_all([sam,frank])

# Can be added separately like below
# db.session.add(sam)
# db.session.add(frank)

db.session.commit()

print(sam.id)
print(frank.id)