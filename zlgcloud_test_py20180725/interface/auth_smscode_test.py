#coding=utf_8
import unittest
import requests

class AuthSmscodeTest(unittest.TestCase):#特殊字符，座机，
    '''获取短信验证码'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/auth/smscode?mobile="
    def tearDown(self):
        print(self.result)

    def test_auth_smscode_all_null(self):
        '''号码为空'''
        payload = ''
        r = requests.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_auth_smscode_lt_11(self):
        '''号码少于11位'''
        payload = '1231234120'
        r = requests.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_auth_smscode_mt_11(self):
        '''号码多于11位'''
        payload = '123123412001'
        r = requests.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_auth_smscode_wrong(self):
        '''号码不存在'''
        payload = '12400000000'
        r = requests.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,403)

    def test_auth_smscode_right(self):
        '''有效号码'''
        payload = '12312341211'
        r = requests.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)

if __name__ == '__main__':
    unittest.main()
