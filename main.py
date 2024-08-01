import csv
from classes import BankCalculator

checking_chase_name = "CheckingChase.CSV"
saving_chase_name = "SavingChase.CSV"
BofA_name = "stmt.csv"


def chase_data(file):
    file = csv.reader(file)
    next(file)

    transactions_dct = {}

    for line in file:
        description = line[2]
        while description in transactions_dct:
            description = "0" + description

        if line[0] == "DEBIT":
            description = " ".join(description.split()[:-1])

        transactions_dct[description] = line[1], float(line[3]), line[5], line[0]

    first_transaction = (list(transactions_dct.values())[-1])
    beginning_date = first_transaction[0]
    beginning_balance = float(first_transaction[2].replace(",", ""))

    last_transaction = (list(transactions_dct.values())[0])
    ending_date = last_transaction[0]
    ending_balance = float(last_transaction[2].replace(",", ""))

    if first_transaction[0] == "DEBIT":
        beginning_balance -= first_transaction[1]
    else:
        beginning_balance -= first_transaction[1]

    data_tuple = (transactions_dct, beginning_date,
                  beginning_balance, ending_date, ending_balance)

    return data_tuple


def bank_of_america(file):
    csv_reader = csv.reader(file)
    next(csv_reader)

    beginning = next(csv_reader)
    beginning_date = beginning[0][-10:]
    beginning_balance = float(beginning[-1])

    total_credits = float(next(csv_reader)[-1].replace(",", ""))
    total_debits = float(next(csv_reader)[-1].replace(",", ""))

    ending = next(csv_reader)
    ending_balance = float(ending[-1].replace(",", ""))
    ending_date = ending[0][-10:]

    next(csv_reader)
    next(csv_reader)
    next(csv_reader)

    transactions_dct = {}

    for line in csv_reader:
        amount = float(line[2].replace(',', ''))
        balance = float(line[3].replace(',', ''))

        description = line[1]
        while description in transactions_dct:
            description = "0" + description

        if amount < 0:
            transactions_dct[description] = line[0], amount, balance, "DEBIT"
        else:
            transactions_dct[description] = line[0], amount, balance, "CREDIT"

    if ending_balance == round(beginning_balance + total_credits + total_debits, 2):
        ending_balance = ending_balance
        beginning_balance = beginning_balance
    else:
        print("\nError: "
              "Ending balance do not match expenses and income")

    data_tuple = (transactions_dct, beginning_date,
                  beginning_balance, ending_date, ending_balance)

    return data_tuple


saving_chase_file = open(saving_chase_name, 'r')
chase_saving_data = (chase_data(saving_chase_file))
ChaseSaving = BankCalculator(chase_saving_data, "Chase Saving Account")
print(ChaseSaving)
saving_chase_file.close()

checking_chase_file = open(checking_chase_name, 'r')
chase_checking_data = (chase_data(checking_chase_file))
ChaseChecking = BankCalculator(chase_checking_data, "Chase Checking Account")
print(ChaseChecking)
checking_chase_file.close()

BofA_file = open(BofA_name, 'r')
BofA_data = bank_of_america(BofA_file)
BofA = BankCalculator(BofA_data, "Bank of America Account")
print(BofA)
BofA_file.close()

# print(BofA + ChaseSaving)
# print(ChaseSaving + ChaseChecking)
print(BofA + ChaseSaving + ChaseChecking)
