class Account:
    hbank_balance = 0
    ibank_balance = 0
    pbank_balance = 0
    total_balance = 0

    @classmethod
    def update_balance(cls, bank, amount, stat):
        if bank == 'hbank':
            if stat == 'income':
                cls.hbank_balance += amount
            else:
                cls.hbank_balance -= amount
            return cls.hbank_balance
        elif bank == 'ibank':
            if stat == 'income':
                cls.ibank_balance += amount
            else:
                cls.ibank_balance -= amount
            return cls.ibank_balance
        elif bank == 'pbank':
            if stat == 'income':
                cls.pbank_balance += amount
            else:
                cls.pbank_balance -= amount
            return cls.pbank_balance
        else:
            raise ValueError("Invalid bank name")
    
    @classmethod
    def total_Balance(cls):
        cls.total_balance = cls.hbank_balance + cls.ibank_balance + cls.pbank_balance
        return cls.total_balance

    def __str__(cls):
        return f'Total balance: {Account.total_Balance()}, hbank: {cls.hbank_balance}, ibank: {cls.ibank_balance}, pbank: {cls.pbank_balance}'
        
# print(Account.update_balance('hbank',1000,100))
# print(Account.update_balance('ibank',1000,200))
# print(Account.update_balance('pbank',1000,300))
# print(Account.update_balance('hbank',2000,200))
# print(Account.update_balance('ibank',2000,300))
# print(Account.update_balance('pbank',2000,400))
# print(Account())

while True:
    transact = input('Enter if the transaction is for hbank or ibank or pbank by inputting 1 or 2 or 3? ')
    if transact == 1:
        bank = 'hbank'
    elif transact == 2:
        bank = 'ibank'
    else:
        bank = 'pbank'
        #incomplete