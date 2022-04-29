from controller.AtmController import AtmController
from model.AtmModel import AtmModel
from config import Config
class app:
    def __init__(self):
        self.atm_model = AtmModel()
        self.atm_controller = AtmController(self.atm_model)
        self.atm_controller.set_pin_regex(Config.pin_format)
    
    def db_init(self):
        """ 데이터베이스를 초기화합니다. """
        self.atm_controller.register_account('111-222-333333', 'SONGYONGWOOK', 10000)
        self.atm_controller.register_account('111-222-333333', 'SONGYONGWOOK2', 2000000)
        self.atm_controller.register_account('111-222-333333', 'SONGYONGWOOK3', 310000)
        self.atm_controller.register_account('000-111-222222', 'PARKSUNGHOON', 770000)
        self.atm_controller.register_account('123-456-333333', 'JUNGJINCHAN', 11000000)
        
    def sample_atm(self, pin_number:str):
        # 테스트를 위한 데이터베이스 초기화
        self.db_init()
        
        # pin번호로 계정 가져오기
        accounts = self.atm_controller.findAccountByValidaePin(pin_number)
        # 계정 선택하기
        sel_account = accounts[0]

        # 계정 잔금 확인
        balance = self.atm_controller.get_balance(sel_account)
        print('계정 잔금 : ', balance)

        # 입금
        money = 100000
        self.atm_controller.deposit(sel_account, money)

        # 입금 후 잔액 조회
        balance = self.atm_controller.get_balance(sel_account)
        print(money, '원 입금 후 잔액 : ', balance)

        # 출금
        money = 20000
        self.atm_controller.withdraw(sel_account, money)

        # 출금 후 잔액 조회
        balance = self.atm_controller.get_balance(sel_account)
        print(money, '원 출금 후 잔액 : ', balance)

if __name__== '__main__':
    application = app()
    input_pin = '111-222-333333'
    application.sample_atm(input_pin)