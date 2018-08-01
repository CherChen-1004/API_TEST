#coding=utf_8
#Author = Cherchan

import unittest
import requests
import threading
from db_fixture.test_data import UsersForTest

'''返回码如下：
            200   操作成功
            400	无效参数
            404	验证码或Token不存在。
            500	服务器错误'''


def recover_password(username,methor,session):
    '''创建获取恢复密码的验证码'''
    payload = username + '&type=' + methor
    r = session.get('https://zlab.zlgcloud.com/v1/auth/recover_password?username='+payload)
    return r.json()['message']

def reset_password_test(url,code,username,password,session):
    payload = {"code": code,"username": username,"password": password}
    r = session.post(url=url,json=payload)
    return r.status_code

class AuthResetPasswordTest(unittest.TestCase):
    '''重置用户密码接口'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com/v1/auth/reset_password"
    def tearDown(self):
        print(self.result)

    def test_auth_reset_password_mobile_right(self):###用实际手机号测试通过
        '''创建一个用户然后传入该用户的用户名及type=mobile到恢复用户密码接口，然后再传入该返回的验证码、用户名、符合规则的新密码'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        code = user.recover_password(username=user.username,type='mobile').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code,username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,200)
    def test_auth_reset_password_email_right(self):
        '''创建一个用户然后传入该用户的用户名及type=email到恢复用户密码接口，然后再传入该返回的验证码、用户名、符合规则的新密码'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        code = user.recover_password(username=user.username,type='email').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code,username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,200)
    def test_auth_reset_password_mobile_code_null(self):
        '''传入的验证码为空'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        self.result = reset_password_test(url=self.base_url,code='',username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,400)
    def test_auth_reset_password_mobile_code_ls(self):
        '''传入的验证码少于6位'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        code = user.recover_password(username=user.username,type='mobile').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code[:-1],username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,400)
    def test_auth_reset_password_email_code_ls(self):
        '''传入的验证码少于6位'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        code = user.recover_password(username=user.username,type='email').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code[:-1],username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,400)
    def test_auth_reset_password_mobile_code_m(self): ###delete
        '''传入的验证码多1位'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        code = user.recover_password(username=user.username,type='email').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code+'1',username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_auth_reset_password_mobile_username_null(self):
        '''传入的用户名为空'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        code = user.recover_password(username=user.username,type='email').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code,username='',password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_auth_reset_password_mobile_password_null(self):
        '''传入的password为空'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = ''
        code = user.recover_password(username=user.username,type='email').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code,username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_auth_reset_password_mobile_password_ls(self):
        '''传入的password少于8位'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc'
        code = user.recover_password(username=user.username,type='email').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code,username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,400)
    def test_auth_reset_password_mobile_password_m(self):
        '''传入的password多于16位'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc_1234567890'
        code = user.recover_password(username=user.username,type='email').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code,username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,400)
    def test_auth_reset_password_email_other_username(self):
        '''恢复密码接口传入其他用户的username'''
        session = requests.Session()
        user1 = UsersForTest(11)
        user1.create_users()
        user = UsersForTest(12,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        code = user.recover_password(username=user.username,type='email').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code,username=user1.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        user1.delete_users()
        self.assertEqual(self.result,400)
    def test_auth_reset_password_mobile_other_username(self):
        '''恢复密码接口传入其他用户的username'''
        session = requests.Session()
        user1 = UsersForTest(11)
        user1.create_users()
        user = UsersForTest(12,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        code = user.recover_password(username=user.username,type='mobile').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code,username=user1.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        user1.delete_users()
        self.assertEqual(self.result,400)
    def test_auth_reset_password_mobile_code_wrong(self):
        '''创建一个用户然后传入该用户的用户名到恢复用户密码接口，然后再传入用户名、符合规则的新密码和一个错误的验证码'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        code = '123456'
        self.result = reset_password_test(url=self.base_url,code=code[:-1],username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,400)
    def test_auth_reset_password_mobile_code_of_other_user(self):
        '''传入其他用户的验证码'''
        session = requests.Session()
        user = UsersForTest(11,session=session)
        user.create_users()
        password = 'ABC_abc_123'
        user1 = UsersForTest(12)
        code = user1.recover_password(username=user1.username,type='mobile').json()['message']
        self.result = reset_password_test(url=self.base_url,code=code[:-1],username=user.username,password=password,session=session)
        if self.result == 200:
            user.password = password
        user.delete_users()
        self.assertEqual(self.result,400)
    # def test_auth_reset_password_mobile_create_n_users(self):    ###该功能用到多线程  移至supplement_test.py中
    #     '''创建多个用户然后依次进行恢复密码，再一一对应重置密码'''
    #     for n in range(100):
    #         session = requests.Session()
    #         user = UsersForTest(n, session)
    #         user.create_users()
    #
    #     def reset_password(num):
    #         session = requests.Session()
    #         username = test_data_arr[num][1]
    #         code = recover_password(username, 'mobile', session)
    #         new_password = '123456789'
    #         payload = {"code": code, "username": username, "password": new_password}
    #         r = session.post(self.base_url, json=payload)
    #         print(r.status_code)
    #         self.result = r.status_code
    #         self.assertEqual(self.result, 200)
    #         session2 = requests.Session()
    #         user = UsersForTest(num, session)
    #         if self.result == 200:
    #             user.password = '123456789'
    #         user.login()
    #         user.delete_users()
    #
    #     threads = []
    #     for n in range(100):
    #         num = n
    #         t = threading.Thread(target=reset_password, args=(num,))
    #         threads.append(t)
    #     for t in threads:
    #         t.setDaemon(True)
    #         t.start()
    #     t.join()

    def test_auth_reset_password_mobile_code_wrong_double(self):
        '''创建两个用户然后依次进行恢复密码，返回的验证码与用户名错开进行重置密码操作'''
        session = requests.Session()
        user_1 = UsersForTest(11,session)
        user_1.create_users()
        user_2 = UsersForTest(12,session)
        user_2.create_users()
        code_1 = user_1.recover_password(user_1.username,'mobile').json()['message']
        code_2 = user_2.recover_password(user_2.username,'mobile').json()['message']
        r1 = user_1.reset_password(code_1,user_1.username,'12345678')
        print('r1',r1.status_code)
        r2 = user_2.reset_password(code_2,user_1.username,'12345678')
        print('r2',r2.status_code)
        r3 = user_1.reset_password(code_1,user_2.username,'12345678')
        print('r3', r3.status_code)
        r4 = user_1.reset_password(code_2,user_2.username,'12345678')
        print('r4', r4.status_code)
        if r1.status_code == 200 or r2.status_code == 200:
            user_1.password = '12345678'
        r5 = user_1.login()
        r6 = user_1.delete_users()
        if r3.status_code == 200 or r4.status_code == 200:
            user_2.password = '12345678'
        r7 = user_2.login()
        r8 = user_2.delete_users()
        self.result = r1.status_code == 400 and r2.status_code == 400 and r3.status_code == 400 and r4.status_code == 200
        self.assertEqual(self.result,True)

if __name__ == '__main__':
    unittest.main(verbosity=2)
