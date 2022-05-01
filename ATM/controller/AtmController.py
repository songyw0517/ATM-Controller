import re
if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/..')
    from __init__ import AtmControllerBase
    from model.AtmModel import AtmModel
    from DTO import Account
else:
    from controller import AtmControllerBase
    from model.AtmModel import AtmModel
    from DTO import Account
    

class AtmController(AtmControllerBase):
    def __init__(self, atm_model:AtmModel):
        super().__init__()
        self.pin_regex = None
        self.atm_model = atm_model

    """ 계정을 등록합니다. """
    def register_account(self, pin_number:str, account:str, balance:int):
        # TypeError, ValueError handling
        if type(pin_number) is not str:
            raise TypeError('pin_number type is str, but now pin_number type is %s'%type(pin_number))
        if type(account) is not str:
            raise TypeError('account type is str, but now account type is %s'%type(account))
        if type(balance) is not int:
            raise TypeError('balance type is int, but now balance type is %s'%type(balance))
        if not self.validate_pin_number_format(pin_number):
            raise ValueError('"pin_number format" not match "set format"')

        accounts = self.atm_model.find_by_pin_num(pin_number)
        for acc in accounts:
            if acc.__dict__['_Account__account']==account:
                raise ValueError('%s is already exist. (duplicate)'%account)
        if balance < 0:
            raise ValueError('balance is positive integer')
        
        new_account = self.atm_model.save_account(pin_number, account, balance)

        return new_account

    """
    핀번호의 정규식을 설정합니다.
    - pin_format을 딕셔너리로 받아 클래스 내의 정규식을 설정합니다.
    """
    def set_pin_regex(self, pin_format:dict):
        if type(pin_format) is not dict:
            raise TypeError('pin_format type is dict, but now pin_format type is %s'%type(pin_format))
        if 'numbers' not in pin_format:
            raise KeyError('numbers is not in pin_format')
        if 'split' not in pin_format:
            raise KeyError('split is not in pin_format')
        if type(pin_format['numbers']) is not list:
            raise TypeError("pin_format['numbers'] type is list, but now pin_format['numbers'] type is %s"
            %type(pin_format['numbers']))
        if type(pin_format['split']) is not str:
            raise TypeError("pin_format['split'] type is str, but now pin_format['split'] type is %s"
            %type(pin_format['split']))
        # 정규식 패턴 생성
        self.pin_regex=""
        for i in range(len(pin_format['numbers'])):
            self.pin_regex+="[0-9]{%d}"%pin_format['numbers'][i]
            if i==len(pin_format):
                break
            self.pin_regex+=pin_format['split']


    """ 핀번호 포맷을 검증합니다. """
    def validate_pin_number_format(self, pin_number:str):
        if type(pin_number) is not str:
            raise TypeError('pin_number type is str, but now pin_number type is %s'%type(pin_number))
        
        if self.pin_regex is None:
            raise KeyError('pin_regex is not set.')

        # 검증이 완료되면 True, 안되면 False를 반환합니다.
        if re.fullmatch(self.pin_regex, pin_number):
            return True
        else:
            return False
    
    """ 핀번호에 해당하는 계정을 반환합니다. """
    def get_account_by_validate_pin_number(self, pin_number:str):
        # 핀번호 포맷을 검사한 후, 계정을 반환합니다.
        if self.validate_pin_number_format(pin_number):
            accounts = self.atm_model.find_by_pin_num(pin_number)
            return accounts
        else:
            raise ValueError("pin_number format is not correct.")

    """ account에 해당하는 계정을 반환합니다. """
    def find_account(self, account):
        return self.atm_model.find_by_account(account)

    """ 입금을 계산하여 반환합니다. """
    def deposit(self, account, money:int,):
        if type(money) is not int:
            raise TypeError('money type is int, but now money type is %s'%type(money))
        if type(account) is not Account:
            raise TypeError('account type is Account, but now account type is %s'%type(account))
        if money<0:
            raise ValueError('money is positive integer')
        
        find_account = self.find_account(account)
        balance = find_account.balance + money
        self.atm_model.update_balance_by_account(account, balance)
        return balance


    """ 출금을 계산하여 반환합니다. """
    def withdraw(self, account, money:int):
        if type(money) is not int:
            raise TypeError('money type is int, but now money type is %s'%type(money))
        if type(account) is not Account:
            raise TypeError('account type is Account, but now account type is %s'%type(account))
        if money<0:
            raise ValueError('money is positive integer')

        find_account = self.find_account(account)        
        # 출금 계산
        balance = find_account.balance - money

        if balance < 0:
            return '잔액이 부족합니다.'
        else:
            self.atm_model.update_balance_by_account(account, balance)
        return balance

    """ 잔고를 조회합니다. """
    def get_balance(self, account):
        if type(account) is not Account:
            raise TypeError('account type is Account, but now account type is %s'%type(account))
        return account.balance



if __name__ == '__main__':
    test = AtmController(AtmModel())
    test.set_pin_regex({
        'numbers' : [3,3,6],
        'split' : '-'
    })
    print(test.validate_pin_number_format("102-854-473382"))