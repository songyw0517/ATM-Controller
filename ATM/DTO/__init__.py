"""
Data Transfer Object를 정의합니다.
"""
class Account:
    def __init__(self, pin_number, account, balance):
        self.__pin_number = pin_number
        self.__account = account
        self.__balance = balance
    
    @property
    def pin_number(self):
        return self.__pin_number

    @property
    def account(self):
        return self.__account

    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, balance):
        self.__balance = balance