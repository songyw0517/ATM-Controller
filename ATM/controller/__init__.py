import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/..')
from abc import ABCMeta, abstractmethod

"""
ATMController의 추상클래스(인터페이스)를 정의합니다.
"""
class AtmControllerBase(metaclass=ABCMeta):
    """ 계정 등록 기능 """
    @abstractmethod
    def register_account(self, pin_number:str, account:str, balance:int):
        pass


    """ pin 번호 포맷 검증 기능"""
    @abstractmethod
    def validate_pin_number_format(self, pin_number:str):
        """
        - pin_number을 입력받아 검증을 수행합니다.
        - 검증이 되면 True를, 안되면 False를 반환합니다.
        """
        pass
    
    """ 검증된 핀번호를 입력받아 계정을 반환하는 기능"""
    @abstractmethod
    def findAccountByValidaePin(self, pin_number:str):
        """
        - 검증된 핀번호를 입력받아 
        핀번호에 해당하는 계정을 반환합니다.
        """
        pass
    
    """ account를 입력받아 account를 반환하는 기능"""
    @abstractmethod
    def findAccountByAccount(self, account):
        """
        - account를 입력받아 model로부터 해당하는 account를 반환합니다.
        """
        pass


    """ 입금 기능 """
    @abstractmethod
    def deposit(self, account, money:int,):
        """
        - account와 money를 입력받아 입금 기능을 수행합니다.
        - 입금 기능을 수행한 결과를 반환합니다.
        """
        pass
    
    """ 출금 기능 """
    @abstractmethod
    def withdraw(self, account, money:int):
        """
        - account와 money를 입력받아 출금 기능을 수행합니다.
        - 출금 기능을 수행한 결과를 반환합니다.
        """
        pass
    
    """ 잔고 조회 기능 """
    @abstractmethod
    def get_balance(self, account):
        """
        - account를 입력받아 해당 계정의 잔고를 반환합니다.
        """
        pass