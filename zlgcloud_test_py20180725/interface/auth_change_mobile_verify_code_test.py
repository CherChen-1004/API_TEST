#coding=utf_8
#Author=CherChan

#已调试，可用
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

class AuthChangeMobileVerifyCodeTest(unittest.TestCase):
    '''获取修改手机号码的验证码'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/auth/change_mobile_verify_code?mobile="
    def tearDown(self):
        print(self.result)

    def test_mobile_verify_code_right(self):
        '''登录后发送正确的新的手机号'''
        session = requests.Session()
        user = UsersForTest(3,session)
        user.create_users()
        user.login()
        user1 = UsersForTest()
        payload = user1.mobile
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.delete_users()

    def test_mobile_verify_code_null(self):
        '''登录后传入手机号为空'''
        session = requests.Session()
        user = UsersForTest(3,session)
        user.create_users()
        user.login()
        payload = ''
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

    def test_mobile_verify_code_ls(self):
        '''登录后发送手机号少于11位'''
        session = requests.Session()
        user = UsersForTest(3,session)
        user.create_users()
        user.login()
        user2 = UsersForTest(4)
        payload = user2.mobile[:-1]
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()
    def test_mobile_verify_code_m(self):
        '''登录后发送手机号多于11位'''
        session = requests.Session()
        user = UsersForTest(3,session)
        user.create_users()
        user.login()
        user1 = UsersForTest(num=4)
        payload = user1.mobile + '1'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()
    def test_mobile_verify_code_not_login(self):
        '''不登陆直接发送正确的手机号'''
        session = requests.Session()
        user = UsersForTest(3,session)
        user.create_users()
        user1 = UsersForTest(num=4)
        payload = user1.mobile + '1'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,401)
        user.login()
        user.delete_users()
    def test_mobile_verify_code_mobile_exist(self):      #存在Bug
        '''登录后直接发送已注册的手机号'''
        session_1 = requests.Session()
        user1 = UsersForTest(3,session_1)
        user1.create_users()
        session_2 = requests.Session()
        user2 = UsersForTest(4,session_2)
        user2.create_users()
        user1.login()
        payload = user2.mobile
        r = session_1.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user1.delete_users()
        user2.login()
        user2.delete_users()
    def test_mobile_verify_code_500(self):
        '''登录后发送不存在的新的手机号'''
        session = requests.Session()
        user = UsersForTest(3,session)
        user.create_users()
        user.login()
        payload = '14400000000'
        r = session.get(self.base_url+payload)
        self.result = r.status_code
        self.assertEqual(self.result,403)
        user.delete_users()

if __name__ == '__main__':
    unittest.main()
