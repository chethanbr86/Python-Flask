class Account:
    hbank_balance = 0
    ibank_balance = 0
    pbank_balance = 0
    total_balance = 0

    @classmethod
    def hbank(cls,income,expense):
        cls.hbank_balance += income 
        cls.hbank_balance -= expense   
        return cls.hbank_balance

    @classmethod
    def ibank(cls,income,expense):
        cls.ibank_balance += income 
        cls.ibank_balance -= expense   
        return cls.ibank_balance

    @classmethod
    def pbank(cls,income,expense):
        cls.pbank_balance += income 
        cls.pbank_balance -= expense   
        return cls.pbank_balance
    
    @classmethod
    def total_Balance(cls):
        cls.total_balance = cls.hbank_balance + cls.ibank_balance + cls.pbank_balance
        return cls.total_balance

    def __str__(cls):
        return f'Total balance: {Account.total_Balance()}, hbank: {cls.hbank_balance}, ibank: {cls.ibank_balance}, pbank: {cls.pbank_balance}'
        #try to return with for along with enumerate

print(Account.hbank(1000,100))
print(Account.ibank(1000,200))
print(Account.pbank(1000,300))
print(Account.hbank(2000,200))
print(Account.ibank(2000,300))
print(Account.pbank(2000,400))
print(Account())