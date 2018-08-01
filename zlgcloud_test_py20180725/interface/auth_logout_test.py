#coding=utf_8
#Author = CherChan

import unittest
import requests
from db_fixture.test_data import UsersForTest
'''返回码如下：
            200 操作成功
            401	没有登录
            500	服务器错误'''

class AuthLogoutTest(unittest.TestCase):
    '''用户退出接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/auth/logout"
    def tearDown(self):
        print(self.result)
    def test_auth_logout_login(self):
        '''登录后退出'''
        session = requests.Session()
        user = UsersForTest(8,session)
        user.create_users()
        user.login()
        r = session.get(self.base_url)
        self.result = r.status_code
        self.assertEqual(self.result, 200)
        user.login()
        user.delete_users()
    def test_auth_logout_not_login(self):
        '''没有登录'''
        session = requests.Session()
        user = UsersForTest(8,session)
        user.create_users()
        # user.login()
        r = session.get(self.base_url)
        self.result = r.status_code
        self.assertEqual(self.result, 401)
        user.login()
        user.delete_users()

    def test_auth_logout_double(self):
        '''退出后再退出'''
        session = requests.Session()
        user = UsersForTest(8,session)
        user.create_users()
        user.login()
        r1 = session.get(self.base_url)
        r = session.get(self.base_url)
        self.result = r.status_code
        self.assertEqual(self.result, 401)
        user.login()
        user.delete_users()


if __name__ == '__main__':
    unittest.main()
