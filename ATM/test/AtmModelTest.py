import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/..')
from unittest import TestCase
from model.AtmModel import AtmModel
import unittest
"""
AtmModel과 관련된 테스트를 수행합니다.
"""
class AtmModelTest(TestCase):
    """ 계정 등록 메소드를 테스트합니다. """
    def test_save_account(self):
        # 테스트 1. 아래와 같은 정보가 주어졌을 때, 저장이 되었는지 확인
        pin_number = '111-222-333333'
        account = 'Song'
        balance = 1000000
        atm_model = AtmModel()
        result = atm_model.save_account(pin_number, account, balance)
        self.assertIn(result, atm_model.repository)
        
    """ pin 번호로 계정을 찾는 메소드를 테스트합니다. """
    def test_find_by_pin_num(self):
        atm_model = AtmModel()
        # 테스트 1. 아래와 같은 계정을 저장한 후,
        # 핀번호가 주어졌을 때 핀번호에 해당하는 객체가 반환되는지 확인
        pin_number = find_pin_number = '111-222-333333'
        account = 'Song'
        balance = 1000000
        result = atm_model.save_account(pin_number, account, balance)
        
        test_result = atm_model.find_by_pin_num(find_pin_number)
        
        self.assertIn(result, test_result)

        # 테스트 2. 같은 핀번호를 가지고 있는 계정이 있을 경우
        # 모두 같은 핀번호인지 확인
        atm_model = AtmModel()
        pin_number = find_pin_number = '111-222-333333'
        account = 'Park'
        balance = 3000000
        
        atm_model.save_account(pin_number, account, balance)

        result = atm_model.find_by_pin_num(find_pin_number)

        for account in result:
            self.assertEqual(account.pin_number, pin_number)

        # 테스트 3. 리포지토리에 없는 핀번호를 주었을 때
        # 빈 리스트가 반환되는지 확인
        atm_model = AtmModel()
        not_exist_pin_num = '12'
        test_result = atm_model.find_by_pin_num(not_exist_pin_num)
        self.assertEqual(test_result, [])

    """ account로 계정을 반환하는 메소드를 테스트합니다. """            
    def test_find_by_account(self):
        # 테스트 1. 리포지토리에 없는 계정을 찾는 경우
        atm_model = AtmModel()
        with self.assertRaises(KeyError):
            atm_model.find_by_account(12)

        # 테스트 2. 데이터를 제대로 가져온 경우
        atm_model = AtmModel()
        pin_number = '111-222-333333'
        account = 'Park'
        balance = 3000000
        result = atm_model.save_account(pin_number, account, balance)
        test = atm_model.find_by_account(result)
        self.assertEqual(result, test)
        
    """ 잔액을 업데이트하는 메소드를 테스트합니다. """
    def test_update_balance_by_account(self):
        # 테스트 1. 아래와 같은 계정을 저장한 후 
        # 반환된 계정과 바꿀 잔액을 update_balance_by_account에 전달
        atm_model = AtmModel()
        pin_number = '111-222-333333'
        account = 'Song'
        balance = 1000000
        find_account = atm_model.save_account(pin_number, account, balance)
        change_balance = 10

        result = atm_model.update_balance_by_account(find_account, change_balance)

        self.assertEqual(result.balance, change_balance)
            
if __name__ == '__main__':
    unittest.main()