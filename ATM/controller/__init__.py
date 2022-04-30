import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/..')
from abc import ABCMeta, abstractmethod

"""
ATMController의 추상클래스(인터페이스)를 정의합니다.
"""
class AtmControllerBase(metaclass=ABCMeta):
    """ 계정 등록 """
    @abstractmethod
    def register_account(self, pin_number:str, account:str, balance:int):
        pass
    
    """ 핀번호 포맷 정규식 설정 """
    def set_pin_regex(self, pin_format:dict):
        """
        - pin_format을 입력받아 정규식을 설정합니다.
        """
        pass

    """ 핀번호 포맷 검증 """
    @abstractmethod
    def validate_pin_number_format(self, pin_number:str):
        """
        - pin_number을 입력받아 검증을 수행합니다.
        - 검증이 되면 True를, 안되면 False를 반환합니다.
        """
        pass
    
    """ 핀번호에 해당하는 계정 반환 """
    def get_account_by_validate_pin_number(self, pin_number:str):
        """
        - pin_number에 대한 검증 수행
        - 검증이 되면 모델에 핀번호에 해당하는 계정을 요청합니다.
        - 모델로부터 받은 계정을 반환합니다. (복수의 계정이 반환될 수 있습니다.)
        """

    """ account를 입력받아 account를 반환 """
    @abstractmethod
    def find_account(self, account):
        """
        - account를 입력받아 모델에 계정에 해당하는 계정을 요청합니다.
        - 모델로부터 받은 계정을 반환합니다. (단 하나의 계정만 반환됩니다.)
        """
        pass


    """ 입금 기능 """
    @abstractmethod
    def deposit(self, account, money:int,):
        """
        - account와 money를 입력받아 입금 기능을 수행합니다.
        - 모델로부터 찾은 계정을 받아, 계정의 데이터를 수정합니다(입금).
        - 이후 모델에 수정된 데이터를 전달하여 데이터를 업데이트합니다.
        - 입금이 완료된 잔액을 반환합니다.
        """
        pass
    
    """ 출금 기능 """
    @abstractmethod
    def withdraw(self, account, money:int):
        """
        - account와 money를 입력받아 출금 기능을 수행합니다.
        - 모델로부터 찾은 계정을 받아, 계정의 데이터를 수정합니다.(출금).
        - 만약 잔액이 부족한 경우, '잔액이 부족합니다' 문자열을 반환합니다.
        - 출금이 성공적으로 이루어지면, 모델에 수정된 데이터를 전달하여 
        데이터를 업데이트합니다.
        - 출금이 완료된 잔액을 반환합니다.
        """
        pass
    
    """ 잔고 조회 기능 """
    @abstractmethod
    def get_balance(self, account):
        """
        - account를 입력받아 모델로부터 계정을 받습니다.
        - 받은 계정의 잔액을 반환합니다.
        """
        pass