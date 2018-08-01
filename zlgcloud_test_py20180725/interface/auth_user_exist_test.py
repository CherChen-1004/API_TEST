#coding=utf_8
#Author = 陈晓霞

import unittest
import requests
from db_fixture.test_data import UsersForTest
'''返回码如下：
            200 操作成功
            400	无效参
            404	用户不存在
            500	服务器错误 '''

class AuthUserExistTest(unittest.TestCase):
    '''判断用户是否存在接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/auth/user_exist?username="
    def tearDown(self):
        print(self.result)
    def test_auth_user_exist_right(self):
        '''创建一个用户后判断该用户的用户是否存在'''
        session = requests.Session()
        user = UsersForTest(11,session)
        user.create_users()
        u = user.username
        payload = u
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.login()
        user.delete_users()

    def test_auth_user_exist_null(self):
        '''传入参数为空'''
        r = requests.get(self.base_url)
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_auth_user_exist_ls_2(self):
        '''用户名小于2位'''
        u = 'a'
        payload = u
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
    def test_auth_user_exist_mt_32(self):       ###存在Bug
        '''用户名more than 32位'''
        u = '01234567890123456789012345679012'
        payload = u
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,404)

    def test_auth_user_exist_m(self):  ###delete
        '''用户名多1位'''
        session = requests.Session()
        user = UsersForTest(13,session)
        user.create_users()
        u = user.username + 'a'
        payload = u
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,404)
        user.login()
        user.delete_users()
    def test_auth_user_exist_l(self):
        '''用户名少1位'''
        session = requests.Session()
        user = UsersForTest(13,session)
        user.create_users()
        u = user.username[:-1]
        payload = u
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,404)
        user.login()
        user.delete_users()


if __name__ == '__main__':
    unittest.main()
