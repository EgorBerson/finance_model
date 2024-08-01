import re


class BankCalculator(object):
    def __init__(self, data, name):
        self.name = name

        self.transactions = data[0]
        self.income = sum(transaction[1] for transaction in data[0].values() if transaction[-1] == "CREDIT")
        self.expenses = sum(transaction[1] for transaction in data[0].values() if transaction[-1] == "DEBIT")
        self.beginning_date = data[1]
        self.beginning_balance = data[2]
        self.ending_date = data[3]
        self.ending_balance = data[4]
        
    def __str__(self):
        str_results = (f"\n{self.name}\n" +
                       self.beginning_date +
                       f"\nBeginning Balance: {self.beginning_balance:,.2f}"
                       f"\nIncome: {self.income:,.2f}"
                       f"\nExpenses: {self.expenses:,.2f}"
                       f"\nEnding Balance: {self.ending_balance:,.2f}\n" +
                       self.ending_date
                       )
        return str_results

    def __add__(self, other):
        united_dct = {**self.transactions, **other.transactions}
        beginning_balance = self.beginning_balance + other.beginning_balance
        ending_balance = self.ending_balance + other.ending_balance

        beginning_date = self.beginning_date
        if self.beginning_date != other.beginning_date:
            print("\nBEGINNING DATES DO NOT MATCH")
            if self.beginning_date > other.beginning_date:
                beginning_date = other.beginning_date

        ending_date = self.ending_date
        if self.ending_date != other.ending_date:
            print("ENDING DATES DO NOT MATCH")
            if self.ending_date < other.ending_date:
                ending_date = other.ending_date

        # Regular expression to match keys ending with digits or digits followed by an "X"
        pattern = re.compile(r'\d+X?$')

        for key in self.transactions:
            # Find common transactions in the other transactions
            common_transaction = [other_key for other_key in other.transactions if
                                  pattern.search(other_key[-9:]) and (key[-9:] in other_key)]
            if common_transaction and pattern.match(key[-9:]):
                del united_dct[key]
                del united_dct[common_transaction[0]]

        if "Total assets of " in self.name:
            name = f"{self.name} and {other.name}"
        else:
            name = f"Total assets of {self.name} and {other.name}"

        data_tuple = (united_dct, beginning_date,
                      beginning_balance, ending_date, ending_balance)
        return BankCalculator(data_tuple, name)
