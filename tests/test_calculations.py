# Tests
import pytest
from app.calculations import add_func, subtract_func,division_func, multiply_func, BankAccount, InsuficientFunds


# fixture
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

# Name for the functions and files matters
# Test prefix required for pytest to auto discover
def test_addition():
    assert add_func(5,3) == 8

@pytest.mark.parametrize("num1, num2, expected", [
    (3,1,2),
    (15,5,10),
    (5,10,-5)
])
def test_subtraction(num1, num2, expected):
    assert subtract_func(num1, num2) == expected

def test_division():
    assert division_func(5,2) == 2.5

def test_multiply():
    assert multiply_func(5,3) == 15

def test_bank_set_initial_amount(bank_account):

    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()

    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    # bank_account = BankAccount(50)

    bank_account.withdraw(20)

    assert bank_account.balance == 30

def test_deposit():
    bank_account = BankAccount(0)

    assert bank_account.balance == 0

    bank_account.deposit(20)

    assert bank_account.balance == 20

def test_collect_interest():
    bank_account = BankAccount(100)

    bank_account.collect_interest()

    assert round(bank_account.balance) == 110

def test_balance_exception(bank_account):
    with pytest.raises(InsuficientFunds): # Can test specific exceptions
        bank_account.withdraw(55)


