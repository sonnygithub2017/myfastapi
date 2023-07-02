def cal_add(a:int, b:int):
  return a + b

def cal_subtract(a:int, b:int):
  return a - b

def cal_multiply(a:int, b:int):
  return a * b

def cal_divide(a:int, b:int):
  return a//b

class InsufficientFund(Exception):
  pass

class BankAccount():
  def __init__(self, starting_balance=0):
    self.balance = starting_balance

  def deposit(self, amount):
    self.balance += amount

  def withdraw(self, amount):
    if amount > self.balance:
      raise InsufficientFund("Insufficient fund in acct")
      #raise Exception("Insufficient fund in acct")
    self.balance -= amount

  def collect_interest(self):
    self.balance *= 1.1