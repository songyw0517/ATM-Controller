import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/..')
from unittest import TestCase
from controller.AtmController import AtmController
from model.AtmModel import AtmModel
import unittest
import random
from config import Config
MAX_MONEY = 100_000_0000
'''
AtmController과 관련된 테스트를 수행합니다.
'''
class AtmControllerTest(TestCase):
    """ 
    핀번호 검증 메소드를 테스트합니다. 
    
    설정된 핀번호 포맷 : XXX-XXX-XXXXXX, X : 숫자
    테스트 핀번호 포맷 : XX-XXX-XXXX, X : 숫자
    - 설정된 핀번호 포맷과 다르기에 에러가 발생해야합니다.
    """
    def test_validate_pin_number_format(self):
        controller = AtmController(AtmModel())
        controller.set_pin_regex({
            'numbers':[3,3,6],
            'split':'-'
        })
        for _ in range(100):
            test_pin_num = "{}{}-{}{}{}-{}{}{}{}".format(
                                                    random.randint(0, 9),
                                                    random.randint(0, 9),
                                                    random.randint(0, 9),
                                                    random.randint(0, 9),
                                                    random.randint(0, 9),
                                                    random.randint(0, 9),
                                                    random.randint(0, 9),
                                                    random.randint(0, 9),
                                                    random.randint(0, 9))
            test_result = controller.validate_pin_number_format(test_pin_num)
            self.assertEqual(test_result, False)
    
    """ 계정 등록 메소드를 테스트합니다."""
    def test_register_account(self):
        # 테스트 1. pin_number가 str이 아닌 경우
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        pin_number = 0
        account = 'song'
        balance = 1000000
        with self.assertRaises(TypeError):
            controller.register_account(pin_number, account, balance)

        # 테스트 2. account가 str이 아닌 경우
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        pin_number = '111-222-333333'
        account = 0
        balance = 1000000
        with self.assertRaises(TypeError):
            controller.register_account(pin_number, account, balance)

        # 테스트 3. balance가 int가 아닌 경우
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        pin_number = '111-222-333333'
        account = 'song'
        balance = '1000000'
        with self.assertRaises(TypeError):
            controller.register_account(pin_number, account, balance)

        # 테스트 4. pin_number의 포맷이 일치하지 않은 아닌 경우
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        pin_number = '111-222'
        account = 'song'
        balance = 1000000
        with self.assertRaises(ValueError):
            controller.register_account(pin_number, account, balance)

        # 테스트 5. account가 중복될 경우
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        pin_number = '111-222-333333'
        account = 'song'
        balance = 1000000
        controller.register_account(pin_number, account, balance)
        pin_number = '111-222-333333'
        account = 'song'
        balance = 100
        with self.assertRaises(ValueError):
            controller.register_account(pin_number, account, balance)

        # 테스트 6. balance가 음수일 경우
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        pin_number = '111-222-333333'
        account = 'song'
        balance = -1000
        with self.assertRaises(ValueError):
            controller.register_account(pin_number, account, balance)
        
        # 테스트 7. 등록 성공
        model = AtmModel()
        controller = AtmController(model)
        controller.set_pin_regex(Config.pin_format)
        pin_number = '111-222-333333'
        account = 'song'
        balance = 1000
        test_result = controller.register_account(pin_number, account, balance)
        result = model.find_by_account(test_result)
        self.assertEqual(test_result, result)

    """
    핀번호 포맷 정규식 설정 메소드를 테스트합니다.
    """
    def test_set_pin_regex(self):
        # 테스트 1. pin_format이 dict가 아닌 경우
        controller = AtmController(AtmModel())
        with self.assertRaises(TypeError):
            controller.set_pin_regex(10)
        
        # 테스트 2. pin_format에 numbers가 없는 경우
        controller = AtmController(AtmModel())
        with self.assertRaises(KeyError):
            controller.set_pin_regex({'split':'-'})
        
        # 테스트 3. pin_format에 split이 없는 경우
        controller = AtmController(AtmModel())
        with self.assertRaises(KeyError):
            controller.set_pin_regex({'numbers':[1,2,3]})

        # 테스트 4. pin_format['numbers']가 list가 아닌 경우
        controller = AtmController(AtmModel())
        test_pinformat = {'numbers':12, 'split':'-'}
        with self.assertRaises(TypeError):
            controller.set_pin_regex(test_pinformat)

        # 테스트 5. pin_format['split']가 str이 아닌 경우
        controller = AtmController(AtmModel())
        test_pinformat = {'numbers':[1,2,3], 'split':10}
        with self.assertRaises(TypeError):
            controller.set_pin_regex(test_pinformat)

        # 테스트 6. 설정이 제대로 되었는지 확인
        test_pinformat = {'numbers':[1,3,2], 'split':'-'}
        controller.set_pin_regex(test_pinformat)
        result = '[0-9]{1}-[0-9]{3}-[0-9]{2}'
        test_result = controller.pin_regex
        self.assertEqual(test_result, result)
    """
    핀번호 포맷 검증 메소드를 테스트합니다.
    """
    def test_validate_pin_number_format(self):
        # 테스트 1. pin_number가 str이 아닌 경우
        controller = AtmController(AtmModel())
        with self.assertRaises(TypeError):
            controller.validate_pin_number_format(12)
        
        # 테스트 2. pin_regex가 정의되지 않은 경우
        controller = AtmController(AtmModel())
        with self.assertRaises(KeyError):
            controller.validate_pin_number_format("123")
    """
    입금 메소드를 테스트합니다.
    """
    def test_deposit(self):
        # 테스트 1. money가 int형이 아닌 경우
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        pin_number = '111-222-333333'
        account = 'song'
        balance = 1000
        test_Account = controller.register_account(pin_number, account, balance)
        with self.assertRaises(TypeError):
            controller.deposit(test_Account, 'test')

        # 테스트 2. account가 Account형이 아닌 경우
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        with self.assertRaises(TypeError):
            controller.deposit(10, 10)

        # 테스트 3. money가 음수인 경우
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        pin_number = '111-222-333333'
        account = 'song'
        balance = 1000
        test_Account = controller.register_account(pin_number, account, balance)
        with self.assertRaises(ValueError):
            controller.deposit(test_Account, -100)

        # 테스트 4. 임의의 숫자에 대한 테스트
        pin_number = '111-222-333333'
        account = 'song'
        for _ in range(100):
            # controller 초기화
            controller = AtmController(AtmModel())
            controller.set_pin_regex(Config.pin_format)
            balance = random.randint(1, MAX_MONEY)
            # 계정 등록
            test_account = controller.register_account(pin_number, account, balance)
            # 임의의 금액 설정
            money = random.randint(1, MAX_MONEY)
            result = balance+money
            test_result = controller.deposit(test_account, money) # 실행
            # 검증
            self.assertEqual(test_result, result)
    
    """
    출금과 관련된 메소드를 테스트합니다.
    """
    def test_withdraw(self):
        # 테스트 1. money가 int형이 아닌경우
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        pin_number = '111-222-333333'
        account = 'song'
        balance = 1000
        test_Account = controller.register_account(pin_number, account, balance)
        with self.assertRaises(TypeError):
            controller.withdraw(test_Account, '123')

        # 테스트 2. account가 Account형이 아닌경우
        controller = AtmController(AtmModel())
        with self.assertRaises(TypeError):
            controller.withdraw(10, 10)

        # 테스트 3. money가 음수인 경우
        controller = AtmController(AtmModel())
        with self.assertRaises(ValueError):
            controller.withdraw(test_Account, -100)
        
        # 테스트 4. 잔액 부족
        controller = AtmController(AtmModel())
        controller.set_pin_regex(Config.pin_format)
        pin_number = '111-222-333333'
        account = 'song'
        balance = 1000
        test_account = controller.register_account(pin_number, account, balance)
        money = 10000
        test_result = controller.withdraw(test_account, money)
        self.assertEqual(test_result, '잔액이 부족합니다.')        
        
        # 테스트 3. 임의의 숫자에 대한 테스트
        pin_number = '111-222-333333'
        account = 'song'
        for _ in range(100):
            # controller 초기화
            controller = AtmController(AtmModel())
            controller.set_pin_regex(Config.pin_format)
            balance = random.randint(1, MAX_MONEY)
            # 계정 등록
            test_account = controller.register_account(pin_number, account, balance)
            # 임의의 금액 설정
            money = random.randint(1, MAX_MONEY)
            result = balance-money

            test_result = controller.withdraw(test_account, money)
            if result < 0:
                # 잔액 부족 메시지가 나오는지 확인
                self.assertEqual(
                    test_result, 
                    "잔액이 부족합니다."
                )
            else:
                # 출금한 이후의 잔액이 나오는지 확인
                self.assertEqual(test_result, result)

    """
    잔액 반환 메소드 테스트
    """
    def test_get_balance(self):
        controller = AtmController(AtmModel())
        with self.assertRaises(TypeError):
            controller.get_balance(12)

# unittest 실행
if __name__ == '__main__':
    unittest.main()