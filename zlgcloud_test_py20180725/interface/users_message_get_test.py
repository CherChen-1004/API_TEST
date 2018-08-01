#coding=utf_8
#Author = Cher Chan

import unittest
import requests
import json
from db_fixture.test_data import UsersForTest
'''返回码如下：
            200  操作成功
            400  无效参数
            401  没有登录
            404  用户不存在
            500  服务器错误'''

class UsersMessageGetTest(unittest.TestCase): #获取其他已存在用户信息，
    '''信息获取接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com/v1/users/"
    def tearDown(self):
        print(self.result)
    def test_users_message_get_right(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username'''
        session = requests.Session()
        user = UsersForTest(20,session)
        user.create_users()
        user.login()
        payload = user.username
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.delete_users()

    def test_users_message_get_1(self):
        '''创建一个用户，用该用户登录，然后传入1位字符的username'''
        session = requests.Session()
        user = UsersForTest(20,session)
        user.create_users()
        user.login()
        payload = 'a'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()
    def test_users_message_get_2(self):
        '''创建一个用户，用该用户登录，然后传入2位字符的username'''
        session = requests.Session()
        user = UsersForTest(20,session)
        user.create_users()
        user.login()
        payload = 'ab'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,404)
        user.delete_users()
    def test_users_message_get_32(self):
        '''创建一个用户，用该用户登录，然后传入等于32位字符的username'''
        session = requests.Session()
        user = UsersForTest(20,session)
        user.create_users()
        user.login()
        payload = '0123456789012345678901234567890123456789012345678901234567890123'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,404)
        user.delete_users()

    def test_users_message_get_65(self):
        '''创建一个用户，用该用户登录，然后传入等于33位字符的username'''
        session = requests.Session()
        user = UsersForTest(20,session)
        user.create_users()
        user.login()
        payload = '01234567890123456789012345678901234567890123456789012345678901234'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()
    def test_users_message_get_not_login(self):
        '''创建一个用户，不登录，直接传入该用户的username'''
        session = requests.Session()
        user = UsersForTest(20,session)
        user.create_users()
        # user.login()
        payload = user.username
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,401)
        user.delete_users()

    def test_users_message_get_logout(self):
        '''创建一个用户，用该用户登录，退出，再传入该用户的username'''
        session = requests.Session()
        user = UsersForTest(20,session)
        user.create_users()
        user.login()
        r1 = session.get("https://zlab.zlgcloud.com:443/v1/auth/logout")
        payload = user.username
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,401)
        user.login()
        user.delete_users()


if __name__ == '__main__':
    unittest.main()
