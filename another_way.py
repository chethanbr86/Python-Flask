#using just python
#maybe follow this - https://youtu.be/HTD86h69PtE?si=yOGcijdoj3U-02G4
class Account:
    hbank_balance = 0
    hbank_list = {}
    ibank_balance = 0
    ibank_list = {}
    pbank_balance = 0
    pbank_list = {}
    total_balance = 0

    @classmethod
    def update_balance(cls, bank, amount, stat, category):
        if bank == 'hbank':
            if stat == 'income':
                cls.hbank_balance += amount
                cls.hbank_list[stat] = {category:cls.hbank_balance}
            else:
                cls.hbank_balance -= amount
                cls.hbank_list[stat] = {category:cls.hbank_balance}
            return cls.hbank_balance
        elif bank == 'ibank':
            if stat == 'income':
                cls.ibank_balance += amount
                cls.ibank_list[stat] = {category:cls.ibank_balance}
            else:
                cls.ibank_balance -= amount
                cls.ibank_list[stat] = {category:cls.ibank_balance}
            return cls.ibank_balance
        elif bank == 'pbank':
            if stat == 'income':
                cls.pbank_balance += amount
                cls.pbank_list[stat] = {category:cls.pbank_balance}
            else:
                cls.pbank_balance -= amount
                cls.pbank_list[stat] = {category:cls.pbank_balance}
            return cls.pbank_balance
    
    @classmethod
    def total_Balance(cls):
        cls.total_balance = cls.hbank_balance + cls.ibank_balance + cls.pbank_balance
        return cls.total_balance

    def __str__(cls):
        return f'Total balance: {Account.total_Balance()}\n hbank: {cls.hbank_list}\n ibank: {cls.ibank_list}\n pbank: {cls.pbank_list}'#\n category: {cls.category_list}'
        
print(Account.update_balance('hbank',1000,'income','sal'))
print(Account.update_balance('ibank',1000,'income','transfer'))
print(Account.update_balance('pbank',1000,'income','RD'))
print(Account.update_balance('hbank',200,'expense','game'))
print(Account.update_balance('ibank',300,'expense','auto'))
print(Account.update_balance('pbank',400,'expense','gold'))
print(Account())