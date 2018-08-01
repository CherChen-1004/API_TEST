#coding=utf_8
#Author = 陈晓霞

import unittest
import requests
from db_fixture.test_data import UsersForTest
'''返回参数列表：
               200  操作成功
               400  无效参数
               401  没有登录
               500  服务器错误'''

class AuthChangePasswordTest(unittest.TestCase):  #先登录再退出再传入，多线程修改，换一个帐号登录，修改之前登录帐号的密码
    '''修改用户密码接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/auth/change_password"
    def tearDown(self):
        print(self.result)
    def test_auth_change_password_right(self):
        '''正确传入参数'''
        session = requests.Session()
        user = UsersForTest(5,session)
        user.create_users()
        user.login()
        old_password = user.password
        new_password = "12345678"
        payload = {"oldpassword": old_password,"password": new_password}
        r = session.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.delete_users()
    def test_auth_change_password_null(self):
        '''创建一个用户后用该用户登录，然后传入旧密码和空的新密码'''
        session = requests.Session()
        user = UsersForTest(5, session)
        user.create_users()
        user.login()
        old_password = user.password
        new_password = ''
        payload = {"oldpassword": old_password, "password": new_password}
        r = session.post(self.base_url, json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 400)
        user.delete_users()

    def test_auth_change_password_new_password_ls(self):
        '''创建一个用户后用该用户登录，然后传入旧密码和少于8个字符的新密码'''
        session = requests.Session()
        user = UsersForTest(5, session)
        user.create_users()
        user.login()
        old_password = user.password
        new_password = "1234567"
        payload = {"oldpassword": old_password, "password": new_password}
        r = session.post(self.base_url, json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 400)
        user.delete_users()

    def test_auth_change_password_new_password_m(self):
        '''创建一个用户后用该用户登录，然后传入旧密码和多于16个字符的新密码'''
        session = requests.Session()
        user = UsersForTest(5, session)
        user.create_users()
        user.login()
        old_password = user.password
        new_password = "01234567890123456"
        payload = {"oldpassword": old_password, "password": new_password}
        r = session.post(self.base_url, json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 400)
        user.delete_users()

    def test_auth_change_password_not_login(self):
        '''不登录直接传入符合规则的旧密码和新密码'''
        session = requests.Session()
        user = UsersForTest(5, session)
        user.create_users()

        old_password = user.password
        new_password = "01234567890123456"
        payload = {"oldpassword": old_password, "password": new_password}
        r = session.post(self.base_url, json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 401)
        user.delete_users()

    def test_auth_change_password_dis(self):   ###check
        '''传入oldpassword错误'''
        session = requests.Session()
        user = UsersForTest(5,session)
        user.create_users()
        user.login()
        old_password = '**********'
        new_password = "12345678"
        payload = {"oldpassword": old_password,"password": new_password}
        r = session.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

if __name__ == '__main__':
    unittest.main()
