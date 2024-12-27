#incomplete
class Account:
    hbank_balance = 0
    ibank_balance = 0
    pbank_balance = 0

    @classmethod
    def hbank(cls,income,expense):
        cls.balance += income 
        cls.income_bank.append(income)
        cls.balance -= expense   
        cls.expense_bank.append(expense)
        cls.bank_dict[category] = {'income': income, 'expense': expense} #instead of income or expense as key, give category as key with if income or expense
        return cls.balance

    @classmethod
    def ibank(cls,income,expense,category):
        cls.balance += income #or Account.balance works
        cls.income_bank.append(income)
        cls.balance -= expense   
        cls.expense_bank.append(expense)
        cls.bank_dict[category] = {'income': income, 'expense': expense}
        return cls.balance

    @classmethod
    def pbank(cls,income,expense,category):
        cls.balance += income #or Account.balance works
        cls.income_bank.append(income)
        cls.balance -= expense   
        cls.expense_bank.append(expense)
        cls.bank_dict[category] = {'income': income, 'expense': expense}
        return cls.balance
    
    @classmethod
    def total_Balance(cls):
        cls.total_balance = cls.hbank_balance + cls.ibank_balance + cls.pbank_balance
        return cls.total_balance

    def __str__(cls):
        return f'Total balance: {cls.total_balance}, hbank: {cls.hbank_balance}, ibank: {cls.ibank_balance}, pbank: {cls.pbank_balance}'
        #try to return with for along with enumerate

print(Account.hbank(1000,10,'sal1'))
print(Account.ibank(1000,20,'exp1'))
print(Account.pbank(1000,30,'sav1'))
print(Account.hbank(2000,20,'sal2'))
print(Account.ibank(3000,30,'exp2'))
print(Account.pbank(4500,40,'sav2'))
print(Account())