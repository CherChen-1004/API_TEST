#coding=utf_8
#Author = 陈晓霞

import unittest
import requests
from db_fixture.test_data import UsersForTest
'''返回码如下：
                200   正常操作
                400	无效参数
                404	电子邮件地址不存在
                500	服务器错误'''

class AuthEmailExistTest(unittest.TestCase):  
    '''判断邮件地址是否存在接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/auth/email_exist?email="
    def tearDown(self):
        print(self.result)

    def test_auth_email_exist_null(self):
        '''邮件地址为空'''
        r = requests.get(self.base_url)
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_auth_email_exist_ls_2(self):
        '''创建一个用户后判断该用户的Email地址是否存在'''
        session = requests.Session()
        user = UsersForTest(6,session)
        user.create_users()
        payload = user.email
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.login()
        user.delete_users()

    def test_auth_email_exist_dis1(self):
        '''无效参数1'''
        payload = "abc"
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_auth_email_exist_dis2(self):
        '''无效参数2'''
        payload = "abc@mail"
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_auth_email_exist_mt_32(self):
        '''邮件地址不存在'''
        payload = "abcdef@mail.com"
        r = requests.get(self.base_url+ payload)
        self.result = r.status_code
        self.assertEqual(self.result,404)

if __name__ == '__main__':
    unittest.main()
