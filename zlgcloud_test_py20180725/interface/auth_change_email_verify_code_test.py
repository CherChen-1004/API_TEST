#coding=utf_8
import unittest
import requests
from db_fixture.test_data import UsersForTest
'''返回码如下：
            200	操作成功
            400	无效参数
            401	没有登录
            403	没有权限
            500	服务器错误'''
#创建测试数据二维数组
test_data_file_name = 'test_data.txt' #存放测试数据的txt文件   备注：需要将文件放在同一目录下
test_data_1D_arr = []
test_data_arr = []
n = 0
# for line in open(test_data_file_name):
#     test_data_1D_arr.append(str(line)[0:-1])
#     test_data_arr.append(test_data_1D_arr[n].split('\t'))
#     n += 1

class AuthChangeEmailVerifyCodeTest(unittest.TestCase):  #设置1s内发送次数
    '''获取修改邮箱的验证码'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/auth/change_email_verify_code?email="
    def tearDown(self):
        print(self.result)
    def test_email_verify_code_right(self):
        '''登录后发送正确的新的Email地址'''
        session = requests.Session()
        user = UsersForTest(0,session)
        user1 = UsersForTest(1,session=session)
        user.create_users()
        user.login()
        payload = user1.email
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.delete_users()

    def test_email_verify_code_null(self):
        '''登录后传入email为空'''
        session = requests.Session()
        user = UsersForTest(1,session)
        user.create_users()
        user.login()
        payload = ''
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

    def test_mobile_verify_code_nonstandard_1(self):
        '''登录后发送不符合规则email地址，xxxxx'''
        session = requests.Session()
        user = UsersForTest(0,session)
        user.create_users()
        user.login()
        payload = 'test12345601'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

    def test_mobile_verify_code_nonstandard_2(self):
        '''登录后发送不符合规则email地址，xxxxx@'''
        session = requests.Session()
        user = UsersForTest(0,session)
        user.create_users()
        user.login()
        payload = 'test12345601@'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

    def test_mobile_verify_code_nonstandard_3(self):
        '''登录后发送不符合规则email地址，xxxxx@mail'''
        session = requests.Session()
        user = UsersForTest(0,session)
        user.create_users()
        user.login()
        payload = 'test12345601@zlg'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

    def test_mobile_verify_code_nonstandard_4(self):
        '''登录后发送不符合规则email地址，xxxxx@mail.'''
        session = requests.Session()
        user = UsersForTest(5,session)
        user.create_users()
        user.login()
        payload = 'test99999991@zlg.'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

    def test_mobile_verify_code_not_login(self):
        '''不登陆直接发送正确的email地址'''
        session = requests.Session()
        user = UsersForTest(6,session)
        user.create_users()
        # user.login()
        payload = 'test99999992@zlg.cn'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,401)
        user.login()
        user.delete_users()

    def test_mobile_verify_code_mobile_exist(self):      #存在Bug
        '''登录后直接发送已注册的Email地址'''
        session_1 = requests.Session()
        user1 = UsersForTest(0,session_1)
        user1.create_users()
        session_2 = requests.Session()
        user2 = UsersForTest(1,session_2)
        user2.create_users()
        user1.login()
        payload = user2.email
        r = session_1.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user1.delete_users()
        user2.login()
        user2.delete_users()
    def test_mobile_verify_code_500(self):
        '''登录后发送不存在的新的email地址'''
        session = requests.Session()
        user = UsersForTest(0,session)
        user.create_users()
        user.login()
        payload = 'test0000000@zlg.cn'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,500)
        user.delete_users()

if __name__ == '__main__':
    unittest.main()
