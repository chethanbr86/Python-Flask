def get_amount1():
    try:
        amount = int(input('Enter the amount: '))
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        return amount
    except ValueError as e:
        print(e)
        return get_amount1() #This is the recurrence (i.e; returning function until input is right)
    
def get_amount2():
    while True:
        amount = input('Enter the amount: ')
        if amount.isdigit() and int(amount) >= 0:
            return int(amount)
        else:
            print("Invalid input. Please enter a non-negative integer.")

amt1 = get_amount1() 
print(amt1)
amt2 = get_amount2() 
print(amt2)