import itertools
from datetime import datetime

from dateutil.parser import ParserError, parse


class Transaction:
    def __init__(self, transaction_type, amount, date):
        self.transaction_type = transaction_type
        self.amount = amount
        self.date = date

    def __repr__(self):
        return f"Transaction_Type: {self.transaction_type}, Amount: {self.amount}, Date: {self.date}"

    def __str__(self):
        return f"Transaction_Type: {self.transaction_type}, Amount: {self.amount}, Date: {self.date}"


class Account:
    def __init__(self, first_name, last_name, email, balance=0.0):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_active = True
        self.balance = balance
        self.transactions = []

    def __repr__(self):
        return (
            f"Name: {self.first_name}, Surname: {self.last_name}, Email: {self.email}, Balance: {self.balance}, "
            f"Is Active: {self.is_active}"
        )

    def __str__(self):
        return (
            f"Name: {self.first_name}, Surname: {self.last_name}, Email: {self.email}, Balance: {self.balance}, "
            f"Is Active: {self.is_active}"
        )


class Bank:
    account_id = itertools.count()

    def __init__(self):
        self.accounts = {}

    def add_account(self, first_name, last_name, email, *args):
        new_account = Account(first_name, last_name, email, *args)
        self.accounts[next(Bank.account_id)] = new_account

    def delete_account(self, account_id):
        self.accounts[account_id].is_active = False

    def show_accounts(self, is_active=True):
        if is_active:
            return {key: val for (key, val) in self.accounts.items() if val.is_active}
        else:
            return {
                key: val for (key, val) in self.accounts.items() if not val.is_active
            }

    def view(self, account_id, is_active=True):
        self._check_account(account_id)
        return f"Account_Id: {account_id}, {self.accounts[account_id]}, {self.accounts[account_id].transactions}"

    def deposit(self, account_id, amount):
        self._check_account(account_id)
        self.accounts[account_id].balance += amount
        self.accounts[account_id].transactions.append(
            Transaction("deposit", amount, datetime.now())
        )

    def withdraw(self, account_id, amount):
        self._check_account(account_id)
        self._check_balance(account_id, amount)
        self.accounts[account_id].balance -= amount
        self.accounts[account_id].transactions.append(
            Transaction("withdraw", amount, datetime.now())
        )

    def transfer(self, transfer_from_id, transfer_to_id, amount):
        self._check_account(transfer_from_id)
        self._check_account(transfer_to_id)
        self._check_balance(transfer_from_id, amount)
        self.accounts[transfer_from_id].balance -= amount
        self.accounts[transfer_to_id].balance += amount
        self.accounts[transfer_from_id].transactions.append(
            Transaction("transfer_out", amount, datetime.now())
        )
        self.accounts[transfer_to_id].transactions.append(
            Transaction("transfer_in", amount, datetime.now())
        )

    def merge_two_accounts(self, first_account_id, second_account_id):
        first_name = f"{self.accounts[first_account_id].first_name}_{self.accounts[second_account_id].first_name}"
        last_name = f"{self.accounts[first_account_id].last_name}_{self.accounts[second_account_id].last_name}"
        email = self.accounts[first_account_id].email
        balance = (
            self.accounts[first_account_id].balance
            + self.accounts[second_account_id].balance
        )

        self.add_account(first_name, last_name, email, balance)
        self.delete_account(first_account_id)
        self.delete_account(second_account_id)

    def _check_balance(self, account_id, amount):
        if amount > self.accounts[account_id].balance:
            raise ValueError("Insufficient funds")

    def _check_account(self, account_id):
        if account_id not in self.accounts:
            raise ValueError(f"Account with ID {account_id} does not exist.")

    def _parse_date(self, date: str) -> datetime:
        try:
            return parse(date, fuzzy=True)
        except ParserError:
            raise ValueError(f"{date} not a valid data")

    def sort(self, date):
        date = self._parse_date(date)
        temp = {}

        for account_id, account in self.accounts.items():
            for trs in account.transactions:
                if trs.date >= date:
                    temp[account_id] = account

        return sorted(
            temp.values(),
            key=lambda x: (
                sum(
                    [
                        t.amount
                        for t in x.transactions
                        if t.transaction_type == "transfer_out"
                        or t.transaction_type == "transfer_in"
                    ]
                ),
                x.first_name,
            ),
            reverse=True,
        )
