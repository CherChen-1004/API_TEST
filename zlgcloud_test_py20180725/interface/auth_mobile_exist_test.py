#coding=utf_8
#Author = Cherchan

import unittest
import requests
from db_fixture.test_data import UsersForTest

'''返回码如下：
                200   正常操作
                400	无效参数
                404	电子邮件地址不存在
                500	服务器错误'''

class AuthMobileExistTest(unittest.TestCase):
    '''判断手机是否存在接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/auth/mobile_exist?mobile="
    def tearDown(self):
        print(self.result)

    def test_auth_mobile_exist_right(self):
        '''创建一个用户后判断该用户的手机号是否存在'''
        session = requests.Session()
        user = UsersForTest(9,session)
        user.create_users()
        payload = user.mobile
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.login()
        user.delete_users()

    def test_auth_mobile_exist_null(self):
        '''手机号为空'''
        r = requests.get(self.base_url)
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_auth_mobile_exist_ls_11(self):
        '''手机号少于11位'''
        mobile = '123134120'
        payload = mobile
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
    def test_auth_mobile_exist_mt_11(self):
        '''手机号多于11位'''
        mobile = '123123412000'
        payload = mobile
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_auth_mobile_exist_m(self):  ##delete
        '''手机号多1位'''
        session = requests.Session()
        user = UsersForTest(9,session)
        user.create_users()
        payload = user.mobile+"1"
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.login()
        user.delete_users()

    def test_auth_mobile_exist_l(self):
        '''手机号少1位'''
        session = requests.Session()
        user = UsersForTest(9,session)
        user.create_users()
        payload = user.mobile[:-1]
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.login()
        user.delete_users()
    def test_auth_mobile_exist_n(self):
        '''传入一个未注册过的用户名'''
        payload = "12312341300"
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,404)

if __name__ == '__main__':
    unittest.main()
