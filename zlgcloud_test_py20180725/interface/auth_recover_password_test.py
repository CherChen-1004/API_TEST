#coding=utf_8
#Author = Cherchan

import unittest
import requests
from db_fixture.test_data import UsersForTest

'''返回码如下：
            200   操作成功
            400	无效参数
            403	没有权限(高频调用)
            404	用户名、邮件地址或电话号码不存在
            500	服务器错误'''

class AuthRecoverPasswordTest(unittest.TestCase):
    '''恢复密码测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/auth/recover_password?username="
    def tearDown(self):
        print(self.result)

    def test_auth_recover_password_mobile(self):
        '''创建一个用户然后传入该用户的用户名和type=mobile'''
        session = requests.Session()
        user = UsersForTest(10,session)
        user.create_users()
        payload = user.username + '&type=mobile'
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.login()
        user.delete_users()

    def test_auth_recover_password_email(self):
        '''创建一个用户然后传入该用户的用户名和type=email'''
        session = requests.Session()
        user = UsersForTest(10,session)
        user.create_users()
        payload = user.username + '&type=email'
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.login()
        user.delete_users()
    def test_auth_recover_password__mobile_username_ls(self):
        '''传入username小于2位'''
        payload = 'a' + '&type=mobile'
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
    def test_auth_recover_password_mobile_username_m(self):
        '''传入username多于32位'''
        payload = 'abcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcde' + '&type=mobile'
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
    def test_auth_recover_password__email_username_ls(self):
        '''传入username小于2位'''
        payload = 'a' + '&type=email'
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
    def test_auth_recover_password_email_username_m(self):
        '''传入username多于32位'''
        payload = 'abcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcde' + '&type=email'
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
    # def test_auth_recover_password_email_not_exist(self):
    #     '''创建用户时填入一个不存在的Email地址，然后传入该用户的用户名和type=email'''

    def test_auth_recover_password_mobile_username_not_exist(self):
        '''传入一个不存在的用户名和type=mobile'''
        payload = 'abcd' + '&type=mobile'
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,404)

    def test_auth_recover_password_email_username_not_exist(self):
        '''传入一个不存在的用户名和type=email'''
        payload = 'abcd' + '&type=email'
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,404)

if __name__ == '__main__':
    unittest.main()

