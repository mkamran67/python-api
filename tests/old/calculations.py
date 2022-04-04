# Sample Tests Functions <- Not tests themselves


class InsuficientFunds(Exception):
    pass

def add_func(num1 : int, num2 : int):
    return num1 + num2

def subtract_func(num1 : int, num2 : int):
    return num1 - num2

def division_func(num1 : int, num2 : int):
    return num1 / num2

def multiply_func(num1 : int, num2 : int):
    return num1 * num2

class BankAccount():
    def __init__(self, starting_balance = 0):
        self.balance = starting_balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if(amount > self.balance):
            raise InsuficientFunds("Not enough in account")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1 
