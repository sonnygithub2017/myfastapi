import pytest
from app.calculations import cal_add, cal_subtract, cal_multiply, \
  cal_divide, BankAccount, InsufficientFund

@pytest.fixture
def zero_bank_acct():
  return BankAccount()

@pytest.fixture
def bank_acct():
  return BankAccount(50)

def test_add():
  print("Test add case")
  assert cal_add(3, 5) == 8, "3 + 5 should be 8"

def test_sub():
  assert cal_subtract(3, 5) == -2 , "3 - 5 should be -2"

def test_mul():
  assert cal_multiply(3, 5) == 15 , "3 * 5 should be 15"

def test_div():
  assert cal_divide(3, 5) == 0 , "3//5 should be 0"

@pytest.mark.parametrize(
  "num1, num2, expected",
  [(1, 2, 3),(4, 5, 9),(4, -4, 0)]  
)
def test_add_param(num1, num2, expected):
  assert cal_add(num1, num2) == expected, f"{num1} + {num2} should be {expected}"

def test_init_balance():
  acct = BankAccount(50)
  assert acct.balance == 50, "balance should be 50"

def test_default_balance():
  acct = BankAccount()
  assert acct.balance == 0, "balance should be 0"

def test_deposit():
  acct = BankAccount(50)
  acct.deposit(30)
  assert acct.balance == 80, "balance should be 80"

def test_withdraw():
  acct = BankAccount(50)
  acct.withdraw(30)
  assert acct.balance == 20, "balance should be 20"

def test_collect_interest():
  acct = BankAccount(50)
  acct.collect_interest()
  assert round(acct.balance, 2) == 55.0, "balance should be 55.0"

def test_init_balance_fixture(bank_acct):
  assert bank_acct.balance == 50, "balance should be 50"

def test_default_balance_fixture(zero_bank_acct):
  assert zero_bank_acct.balance == 0, "balance should be 0"

def test_deposit_fixture(bank_acct):
  bank_acct.deposit(30)
  assert bank_acct.balance == 80, "balance should be 80"

def test_withdraw_fixture(bank_acct):
  bank_acct.withdraw(30)
  assert bank_acct.balance == 20, "balance should be 20"

def test_collect_interest_fixture(bank_acct):
  bank_acct.collect_interest()
  assert round(bank_acct.balance, 2) == 55.0, "balance should be 55.0"

@pytest.mark.parametrize("deposit, withdraw, expected",
                         [(200, 100, 100),
                          (50, 10, 40),
                          (1200, 200, 1000)])
def test_transaction(zero_bank_acct, deposit, withdraw, expected):
  zero_bank_acct.deposit(deposit)
  zero_bank_acct.withdraw(withdraw)
  assert zero_bank_acct.balance == expected, "failed on transaction test"

def test_insufficient_exeception(bank_acct):
  with pytest.raises(InsufficientFund):  # expected InsufficientFund
    bank_acct.withdraw(200)