from user import User

users = [User(1,'Jose','mypassword'), User(2,'Mimi','password')]

username_table = {u.username: u for u in users} #can be done through for loop normally
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None) #since its a dictonary
    if user and password == user.password:
        return user

def identity(payload): #copying from Flask-JWT website
    user_id = payload['identity']
    return userid_table.get(user_id, None)
