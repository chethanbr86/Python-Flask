#Refer oop_project in 01-Python folder for question

class Account():
    def __init__(self,owner,balance):
        self.owner = owner
        self.balance = balance

    def __repr__(self):
        return f'{self.owner}, {self.balance}'

    def deposit(self, amt_deposited):
        #self.balance = self.balance + amt_deposited
        return self.balance + amt_deposited

    def withdraw(self, amt_withdrawn):
        if self.balance < amt_withdrawn:
            print('Error, withdrawal amount exeeds balance amount')
        return self.balance -  amt_withdrawn

acct1 = Account('Chethan', 0)
print(acct1)

# print(acct1.owner)
print(acct1.balance)
print(acct1.withdraw(500))
print(acct1.deposit(750))
print(acct1.withdraw(5000))

#Doesn't make sense of adding and withdrawl since the above code is not able to update main balance
#probably make a new variable to update balance


