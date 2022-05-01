if __name__ == '__main__':
    from __init__ import AtmModelBase
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/..')
    from DTO import Account
else:
    from model import AtmModelBase
    from DTO import Account


class AtmModel(AtmModelBase):
    def __init__(self):
        super().__init__()
        self.repository = []
    """ 
    계정을 생성하고 저장합니다.
    입력된 변수는 컨트롤러에 의해 검증되었습니다.
    """
    def save_account(self, pin_number, account, balance):
        new_account = Account(pin_number, account, balance)
        self.repository.append(new_account)
        return new_account

    """
    pin_num에 해당하는 계정들을 찾습니다.
    핀번호는 컨트롤러에 의해 검증되었습니다.
    """
    def find_by_pin_num(self, pin_num: str):
        result = []
        for account in self.repository:
            if pin_num==account.pin_number:
                result.append(account)
        return result

    """
    account에 해당하는 계정을 찾습니다.
    account는 컨트롤러에 의해 검증되었습니다.
    """
    def find_by_account(self, account):
        if account in self.repository:
            account_idx = self.repository.index(account)
            return self.repository[account_idx]
        else:
            raise KeyError("account not found.")

    """
    account의 잔액을 balance로 업데이트합니다.
    입력된 변수는 컨트롤러에 의해 검증되었습니다.
    """
    def update_balance_by_account(self, account:Account, balance:int):
        find_account = self.find_by_account(account)
        find_account.balance = balance
        return account



if __name__ == '__main__':
    atm_model = AtmModel()
    atm_model.save_account('1212', 'Song', 1212)
    atm_model.save_account('12', 'Song', 1212)
    atm_model.save_account('22', 'Song', 1212)
    atm_model.save_account('33', 'Song', 1212)
    atm_model.save_account('1212', 'Seo', 10000)
    print("find_by_pin_num")
    result = atm_model.find_by_pin_num('1212')
    
    atm_model.update_balance_by_account(result[1], 1)
    
    
    for account in result:
        print(account.__dict__)
    print('show all')
    atm_model.show_all()