income_balance = 0
def income_amt(income_balance):
    input_amt = int(input('Adding to account Rs.: '))    
    income_balance = income_balance + input_amt
    return income_balance

print(income_amt(income_balance))