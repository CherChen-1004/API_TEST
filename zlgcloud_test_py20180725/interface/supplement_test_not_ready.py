#coding=utf_8
#Author=Cher Chan

import requests
import unittest
from db_fixture.test_data import test_data_arr, device_event_test_data_arr,device_event_test_data_arr, device_model_arr, device_data_arr  ##导入测试数据
from db_fixture.test_data import UsersForTest ##导入各接口类
from db_fixture.test_data import InitialData ##导入初始化数据类

class SupplementTest(object):
    '''补充单个接口测试未能实现的测试用例'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/users"
    def tearDown(self):
        print(self.result)
    def delete_users_then_login(self):
        '''创建一个用户后，删除用户，然后用该用户登录'''
        user =
    def test_auth_reset_password_mobile_create_n_users(self):    ###该功能用到多线程
        '''创建多个用户然后依次进行恢复密码，再一一对应重置密码'''
        for n in range(100):
            session = requests.Session()
            user = UsersForTest(n, session)
            user.create_users()

        def reset_password(num):
            session = requests.Session()
            username = test_data_arr[num][1]
            code = recover_password(username, 'mobile', session)
            new_password = '123456789'
            payload = {"code": code, "username": username, "password": new_password}
            r = session.post(self.base_url, json=payload)
            print(r.status_code)
            self.result = r.status_code
            self.assertEqual(self.result, 200)
            session2 = requests.Session()
            user = UsersForTest(num, session)
            if self.result == 200:
                user.password = '123456789'
            user.login()
            user.delete_users()

        threads = []
        for n in range(100):
            num = n
            t = threading.Thread(target=reset_password, args=(num,))
            threads.append(t)
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()