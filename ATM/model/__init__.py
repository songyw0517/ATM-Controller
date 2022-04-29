from abc import ABCMeta, abstractmethod
class AtmModelBase(metaclass=ABCMeta):
    """
    계정을 리포지토리(db)에 저장하는 메소드
    """
    @abstractmethod
    def save_account(
                    self, 
                    pin_number:str, 
                    account:str, 
                    balance:int):
        pass

    """
    pin번호를 입력받아 해당하는 계정들을 반환
    """
    @abstractmethod
    def find_by_pin_num(self, pin_num:str):
        pass

    """
    account를 입력받아 해당하는 계정하나를 반환
    """
    def find_by_account(self, account):
        """
        계정과 완전히 같은 객체를 반환합니다.
        """
        pass
    """
    Account 객체를 받아 객체의 balance를 수정
    """
    @abstractmethod
    def update_balance_by_account(self, account, balance:int):
        pass
    
    """
    모든 계정을 보여주는 메소드
    """
    @abstractmethod
    def show_all(self):
        pass