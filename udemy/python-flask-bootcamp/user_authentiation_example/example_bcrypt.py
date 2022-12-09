from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
password = 'supersecretpassword'
print(password)

hashed_password = bcrypt.generate_password_hash(password=password)
print(hashed_password)

check = bcrypt.check_password_hash(hashed_password,'supersecretpassword') #wrongpassword put this to get False
print(check)