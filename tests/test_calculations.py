# Tests

from app.calculations import add_func, subtract_func,division_func, multiply_func

# Name for the functions and files matters
# Test prefix required for pytest to auto discover
def test_addition():
    assert add_func(5,3) == 8

def test_subtraction():
    assert subtract_func(5,3) == 2

def test_division():
    assert division_func(5,2) == 2.5

def test_multiply():
    assert multiply_func(5,3) == 15