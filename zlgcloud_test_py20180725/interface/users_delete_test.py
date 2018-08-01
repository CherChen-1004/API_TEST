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
            403  没有权限
            404  用户不存在
            500  服务器错误'''
def delete_users(username,session):
    '''用于删除测试时产生的数据，避免污染数据库'''
    r = session.delete('https://zlab.zlgcloud.com:443/v1/users/'+username)

class UserDeleteTest(unittest.TestCase):
    '''删除用户接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/users/"
    def tearDown(self):
        print(self.result)
    def test_user_delete_right(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username'''
        session = requests.Session()
        user= UsersForTest(15,session)
        username = user.username
        payload = username
        user.create_users()
        user.login()
        r = session.delete(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.delete_users()

    def test_user_delete_null(self):
        '''创建一个用户，用该用户登录，然后传入参数为空'''
        session = requests.Session()
        user= UsersForTest(15,session)
        username = user.username
        payload = ''
        user.create_users()
        user.login()
        r = session.delete(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,405)
        user.delete_users()

    def test_user_delete_1(self):
        '''创建一个用户，用该用户登录，然后传入用户名1位字符'''
        session = requests.Session()
        user= UsersForTest(15,session)
        username = user.username
        payload = 'a'
        user.create_users()
        user.login()
        r = session.delete(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

    def test_user_delete_2(self):
        '''创建一个用户，用该用户登录，然后传入用户名等于2位字符'''
        session = requests.Session()
        user= UsersForTest(15,session)
        username = user.username
        payload = 'ab'
        user.create_users()
        user.login()
        r = session.delete(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,403)
        user.delete_users()

    def test_user_delete_32(self):
        '''创建一个用户，用该用户登录，然后传入用户名等于32位字符'''
        session = requests.Session()
        user= UsersForTest(15,session)
        username = user.username
        payload = '0123456789012345678901234567890123456789012345678901234567890123'
        user.create_users()
        user.login()
        r = session.delete(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,403)
        user.delete_users()

    def test_user_delete_33(self):
        '''创建一个用户，用该用户登录，然后传入用户名等于33位字符'''
        session = requests.Session()
        user= UsersForTest(15,session)
        username = user.username
        payload = '01234567890123456789012345678901234567890123456789012345678901234'
        user.create_users()
        user.login()
        r = session.delete(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

    def test_user_delete_not_login(self):
        '''创建一个用户，不登录，直接传入该用户的用户名'''
        session = requests.Session()
        user= UsersForTest(15,session)
        username = user.username
        payload = username
        user.create_users()
        r = session.delete(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,401)
        user.delete_users()

    def test_user_delete_not_logout(self):
        '''创建一个用户，登录，然后退出，再传入该用户的username'''
        session = requests.Session()
        user= UsersForTest(15,session)
        username = user.username
        payload = username
        user.create_users()
        user.login()
        r1 = session.get("https://zlab.zlgcloud.com:443/v1/auth/logout")
        r = session.delete(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,401)
        user.login()
        user.delete_users()

    def test_user_delete_other_username(self):
        '''创建一个用户，登录，再传入其他用户的username'''
        session_1 = requests.Session()
        user_1 = UsersForTest(15,session_1)
        user_1.create_users()
        session = requests.Session()
        user = UsersForTest(16,session)
        user.create_users()
        username = user_1.username
        payload = username
        user.login()
        r = session.delete(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,403)
        user.login()
        user.delete_users()
        user_1.login()
        user_1.delete_users()


if __name__ == '__main__':
    unittest.main()
