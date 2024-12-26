class Account:
    balance = 0
    income_bank = [] #convert to dict along with category
    expense_bank = [] #convert to dict along with category
    bank_dict = {}

    @classmethod
    def hbank(cls,income,expense,category):
        cls.balance += income #or Account.balance works
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

    def __str__(cls):
        return f'Account balance: {cls.balance}, income: {cls.income_bank}, expense: {cls.expense_bank}, bank_dict: {cls.bank_dict}'
        #try to return with for along with enumerate

print(Account.hbank(1000,10,'sal1'))
print(Account.ibank(1000,20,'exp1'))
print(Account.pbank(1000,30,'sav1'))
print(Account.hbank(2000,20,'sal2'))
print(Account.ibank(3000,30,'exp2'))
print(Account.pbank(4500,40,'sav2'))
print(Account())