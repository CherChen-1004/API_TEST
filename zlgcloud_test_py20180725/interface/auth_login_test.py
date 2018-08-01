#coding=utf_8
#Author = CherChan

import unittest
import requests
import json
from db_fixture.test_data import UsersForTest
'''返回码如下：
            200 操作成功
            400	无效参数
            403	没有权限(高频调用)
            404	用户不存在
            500	服务器错误'''

def delete_users(username,session):
    '''用于删除测试时产生的数据，避免污染数据库'''
    r = session.delete('https://zlab.zlgcloud.com:443/v1/users/'+username)

class AuthLoginTest(unittest.TestCase):  ###用户名与密码不匹配，
    '''登录接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/auth/login"
    def tearDown(self):
        print(self.result)

    def test_auth_login_right(self):
        '''传入正确完整参数'''
        session = requests.Session()
        user = UsersForTest(7,session)
        user.create_users()
        username = user.username
        password = user.password
        payload = {"username": username, "password": password}
        r = session.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 200)
        delete_users(username,session)
    def test_auth_login_all_null(self):
        '''传入参数为空'''
        username = ""
        password = ""
        payload = { "username": username,"password": password}
        r = requests.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
    def test_auth_login_username_null(self):
        '''传入username为空'''
        session = requests.Session()
        user = UsersForTest(7,session)
        user.create_users()
        username = ''
        password = user.password
        payload = {"username": username, "password": password}
        r = session.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 400)
        user.login()
        user.delete_users()

    def test_auth_login_password_null(self):
        '''传入password为空'''
        session = requests.Session()
        user = UsersForTest(7,session)
        user.create_users()
        username = user.username
        password = ''
        payload = {"username": username, "password": password}
        r = session.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 400)
        user.login()
        user.delete_users()

    def test_auth_login_username_1(self):
        '''1位字符'''
        session = requests.Session()
        user = UsersForTest(7,session)
        user.create_users()
        username = 'a'
        password = user.password
        payload = {"username": username, "password": password}
        r = session.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 400)
        user.login()
        user.delete_users()
    def test_auth_login_username_m(self):
        '''传入用户名多于32'''
        session = requests.Session()
        user = UsersForTest(7,session)
        user.create_users()
        username = '01234567890123456789012345678901234567890123456789012345678901234'
        password = user.password
        payload = {"username": username, "password": password}
        r = session.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 400)
        user.login()
        user.delete_users()

    def test_auth_login_password_ls(self):
        '''传入password少于8位'''
        session = requests.Session()
        user = UsersForTest(7,session)
        user.create_users()
        username = user.username
        password = '1234567'
        payload = {"username": username, "password": password}
        r = session.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 400)
        user.login()
        user.delete_users()

    def test_auth_login_password_m(self):
        '''传入password多于16位'''
        session = requests.Session()
        user = UsersForTest(7,session)
        user.create_users()
        username = user.username
        password = '01234567890123456'
        payload = {"username": username, "password": password}
        r = session.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 400)
        user.login()
        user.delete_users()
    def test_auth_login_user_not_exist(self):    ####存在Bug
        '''传入未注册的帐号'''
        session = requests.Session()
        user = UsersForTest(7,session)
        username = user.username
        password = user.password
        payload = {"username": username, "password": password}
        r = requests.post(self.base_url,json=payload)
        self.result = r.status_code
        self.assertEqual(self.result, 404)


if __name__ == '__main__':
    unittest.main()
