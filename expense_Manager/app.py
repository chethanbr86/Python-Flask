class Account:
    income_bank = [] 
    expense_bank = [] 
    bank_dict = {}
    hbalance,ibalance,pbalance = 0,0,0
    total_balance = 0

    @classmethod
    def hbank(cls,income,expense,category):
        cls.hbalance += income  #hbalance cannot be used here, should i initiate it as class variable?
        cls.income_bank.append(income)
        cls.hbalance -= expense   
        cls.expense_bank.append(expense)
        cls.bank_dict[category] = {'income': income, 'expense': expense} 
        cls.total_balance = cls.hbalance
        return f'hbalance: {cls.hbalance}'

    @classmethod
    def ibank(cls,income,expense,category):
        cls.ibalance += income 
        cls.income_bank.append(income)
        cls.ibalance -= expense   
        cls.expense_bank.append(expense)
        cls.bank_dict[category] = {'income': income, 'expense': expense}
        cls.total_balance = cls.ibalance
        return f'ibalance: {cls.ibalance}'

    @classmethod
    def pbank(cls,income,expense,category):
        cls.pbalance += income 
        cls.income_bank.append(income)
        cls.pbalance -= expense   
        cls.expense_bank.append(expense)
        cls.bank_dict[category] = {'income': income, 'expense': expense}
        cls.total_balance = cls.pbalance
        return f'pbalance: {cls.pbalance}'

    def __str__(cls):
        return f'Total Balance: {cls.total_balance}\n income: {cls.income_bank}\n expense: {cls.expense_bank}\n bank_dict: {cls.bank_dict}'
        #try to return with 'for' along with enumerate

print(Account.hbank(10,2,'sal1'))
print(Account.ibank(20,4,'exp1'))
print(Account.pbank(30,6,'sav1'))
print(Account.hbank(15,1,'sal2'))
print(Account.ibank(30,3,'exp2'))
print(Account.pbank(45,5,'sav2'))
print(Account())