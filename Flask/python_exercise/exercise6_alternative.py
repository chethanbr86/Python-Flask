class Account():
    def __init__(self,owner,balance):
        self.owner = owner
        self.balance = balance

    def __repr__(self):
        return f'{self.owner}, {self.balance}'

    def deposit(self, amt_deposited):
        self.balance = self.balance + amt_deposited
        return self.balance

    def withdraw(self, amt_withdrawn):
        if self.balance < amt_withdrawn:
            return 'Error, withdrawal amount exeeds balance amount'
        else:    
            self.balance = self.balance -  amt_withdrawn
            return self.balance

acct1 = Account('Chethan', 1000)
print(acct1)

# print(acct1.owner)
print(acct1.balance)
print(acct1.withdraw(500))
print(acct1.deposit(750))
print(acct1.withdraw(500))

#This is correct compared to original program