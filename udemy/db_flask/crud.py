from sql_py import db, puppy

# create new entry
my_puppy = puppy('Rufus',5)
db.session.add(my_puppy)
db.session.commit()

# Read
all_puppies = puppy.query.all() #list of puppy objects in table
print(all_puppies)

# Selecting by id
puppy_one = puppy.query.get(2)
print(puppy_one.name, puppy_one.age)

# Filters
puppy_frankie = puppy.query.filter_by(name='Frankie')
print(puppy_frankie.all())

# Update
first_puppy = puppy.query.get(1)
first_puppy.age = 6
db.session.add(first_puppy)
db.session.commit()

# Delete
second_pup = puppy.query.get(3)
db.session.delete(second_pup)
db.session.commit()

all_puppies = puppy.query.all() 
print(all_puppies)


