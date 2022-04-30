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
        if not isinstance(pin_number, str):
            raise TypeError('pin_number type is str, but now pin_number type is %s'%type(pin_number))
        if not isinstance(account, str):
            raise TypeError('account type is str, but now account type is %s'%type(account))
        if not isinstance(balance, int):
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
    pin 번호의 정규식을 설정합니다.
    - pin_format을 딕셔너리로 받아 클래스 내의 정규식을 설정합니다.
    """
    def set_pin_regex(self, pin_format:dict):
        if type(pin_format) is not dict:
            raise ValueError('pin_format은 dict형입니다.')
        if 'numbers' not in pin_format:
            raise KeyError("numbers 키가 없습니다.")
        if 'split' not in pin_format:
            raise KeyError("split 키가 없습니다.")

        # 정규식 패턴 생성
        self.pin_regex=""
        for i in range(len(pin_format['numbers'])):
            self.pin_regex+="[0-9]{%d}"%pin_format['numbers'][i]
            if i==len(pin_format):
                break
            self.pin_regex+=pin_format['split']

    

    """ pin 번호 포맷을 검증합니다. """
    def validate_pin_number_format(self, pin_number:str):
        if type(pin_number) is not str:
            raise ValueError('pin_number은 str형입니다.')
        if self.pin_regex is None:
            raise ValueError('pin_regex가 정의되지 않았습니다.')

        # 검증이 완료되면, 해당 핀번호에 해당하는 계정을 반환합니다.
        if re.fullmatch(self.pin_regex, pin_number):
            return True
        else:
            return False
    
    def get_account_by_validate_pin_number(self, pin_number:str):
        if self.validate_pin_number_format(pin_number):
            accounts = self.atm_model.find_by_pin_num(pin_number)
            return accounts
        else:
            raise ValueError("pin_number의 포맷이 다릅니다.")

    def find_account(self, account):
        return self.atm_model.find_by_account(account)

    """ 입금을 계산하여 반환합니다. """
    def deposit(self, account, money:int,):
        if type(money) is not int:
            raise ValueError('money는 int형입니다.')
        if type(account) is not Account:
            raise ValueError('account는 Account형입니다.')
        if money<0:
            raise ValueError('money는 양의 정수입니다.')
        
        find_account = self.find_account(account)
        balance = find_account.balance + money
        self.atm_model.update_balance_by_account(account, balance)
        return balance


    """ 출금을 계산하여 반환합니다. """
    def withdraw(self, account, money:int):
        if type(money) is not int:
            raise ValueError('money는 int형입니다.')
        if type(account) is not Account:
            raise ValueError('account는 Account형입니다.')
        if money<0:
            raise ValueError('money는 양의 정수입니다.')

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
        find_account = self.atm_model.find_by_account(account)
        return find_account.balance



if __name__ == '__main__':
    test = AtmController(AtmModel())
    test.set_pin_regex({
        'numbers' : [3,3,6],
        'split' : '-'
    })
    print(test.validate_pin_number_format("102-854-473382"))