class deposit():

    def income_amt(self):
        input_amt = int(input('Adding to account Rs.: '))    
        self.income_balance = 0
        income_balance = income_balance + input_amt
        print(income_balance)

    def balance_amt(self,income_balance):
        self.income_balance = 0
        self.total_Balance = income_balance
        print(self.total_Balance)
    
    income_amt()
    balance_amt()