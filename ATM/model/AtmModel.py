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
    입력값을 통해 계정을 생성하고 리포지토리에 저장합니다. 
    입력된 pin_number, account, balance는 AtmController에 의해 검증되었습니다.
    """
    def save_account(self, pin_number, account, balance):        
        new_account = Account(pin_number, account, balance)
        self.repository.append(new_account)
        return new_account

    """
    pin 번호를 입력받아, pin_num에 해당하는 계정들을 반환합니다.
    pin 번호는 AtmController에 의해 검증되었습니다.
    """
    def find_by_pin_num(self, pin_num: str):
        result = []
        for account in self.repository:
            if pin_num==account.pin_number:
                result.append(account)
        return result

    """
    account를 입력받아, account에 해당하는 계정을 반환합니다.
    """
    def find_by_account(self, account):
        if account in self.repository:
            account_idx = self.repository.index(account)
            return self.repository[account_idx]
        else:
            raise KeyError("account에 해당하는 계정이 없습니다.")



    """
    account와 balance를 입력받아, account의 잔액을 balance로 수정합니다.
    """
    def update_balance_by_account(self, account:Account, balance:int):
        find_account = self.find_by_account(account)
        find_account.balance = balance
        return account

    def show_all(self):
        for account in self.repository:
            print(account.__dict__)

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