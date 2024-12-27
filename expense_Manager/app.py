class Account:
    hbank_balance = 0
    ibank_balance = 0
    pbank_balance = 0
    total_balance = 0
    category_list = []

#Here all the variables are called within single function, we can make 2 classes (inheritance) one for Account (just bank) and other class for 3 functions amount, category, date within class
#And also take input within the function rather than outside
#https://youtu.be/Dn1EjhcQk64?si=2mxecIq8Twdu37FB - follow for the output type without excel
    @classmethod
    def update_balance(cls, bank, amount, stat, category):
        if bank == 'hbank':
            if stat == 'income':
                cls.hbank_balance += amount
                cls.category_list.append(category)
            else:
                cls.hbank_balance -= amount
                cls.category_list.append(category)
            return cls.hbank_balance
        elif bank == 'ibank':
            if stat == 'income':
                cls.ibank_balance += amount
                cls.category_list.append(category)
            else:
                cls.ibank_balance -= amount
                cls.category_list.append(category)
            return cls.ibank_balance
        elif bank == 'pbank':
            if stat == 'income':
                cls.pbank_balance += amount
                cls.category_list.append(category)
            else:
                cls.pbank_balance -= amount
                cls.category_list.append(category)
            return cls.pbank_balance
        else:
            raise ValueError("Invalid bank name")
    
    @classmethod
    def total_Balance(cls):
        cls.total_balance = cls.hbank_balance + cls.ibank_balance + cls.pbank_balance
        return cls.total_balance

    def __str__(cls):
        return f'Total balance: {Account.total_Balance()}, hbank: {cls.hbank_balance}, ibank: {cls.ibank_balance}, pbank: {cls.pbank_balance}, category: {cls.category_list}'
        
print(Account.update_balance('hbank',1000,'income','sal'))
print(Account.update_balance('ibank',1000,'income','transfer'))
print(Account.update_balance('pbank',1000,'income','RD'))
print(Account.update_balance('hbank',200,'expense','game'))
print(Account.update_balance('ibank',300,'expense','auto'))
print(Account.update_balance('pbank',400,'expense','gold'))
print(Account())

# while True:
#     transact = input('Enter if the transaction is for hbank or ibank or pbank by inputting 1 or 2 or 3? ')
#     if transact == 1:
#         bank = 'hbank'
#     elif transact == 2:
#         bank = 'ibank'
#     else:
#         bank = 'pbank'
#         #incomplete