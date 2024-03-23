income_balance = 0
def income_amt():
    input_amt = int(input('Adding to account Rs.: '))    
    global income_balance
    income_balance = income_balance + input_amt
    return income_balance

total_Balance = print(income_amt())
print(total_Balance)