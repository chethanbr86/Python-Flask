from werkzeug.security import generate_password_hash, check_password_hash

hashed_pass = generate_password_hash('mypassword')
print(hashed_pass)

check = check_password_hash(hashed_pass, 'mypassword') #otherpassword
print(check)

#you can directly work like this instead of calling as in bcrypt, this way also works in bcrypt