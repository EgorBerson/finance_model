import csv
from classes import BankCalculator


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


def make_transaction():
    '911PEPSIVEN9147678600 LANSING MI': ('08/24/2023', -2.0, '135.14', 'DEBIT')
    transaction_name, date, amount, balance, deb_cre

def account_creator(file_name, function, name):
    opened_file = open(file_name, 'r')
    data = function(opened_file)
    print(data)
    print()
    account = BankCalculator(data, name)
    opened_file.close()
    return account


def save_data(data):
    with open("result.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    return True


def load_data():
    with open("result.csv", 'r') as file:
        reader = csv.reader(file)



if __name__ == "__main__":
    checking_chase_name = "CheckingChase.CSV"
    saving_chase_name = "SavingChase.CSV"
    BofA_name = "stmt.csv"

    saving_chase = account_creator(saving_chase_name, chase_data, "Chase Saving Account")
    checking_chase = account_creator(checking_chase_name, chase_data, "Checking Chase Account")
    BofA = account_creator(BofA_name, bank_of_america, "Bank of America Account")

    # print(saving_chase)
    # print(checking_chase)
    # print(BofA)
    # print(BofA + saving_chase + checking_chase)
