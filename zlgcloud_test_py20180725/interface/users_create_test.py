#coding=utf_8
#Author = 陈晓霞
import unittest
import requests
import json
from time import sleep
import time

from db_fixture.test_data import UsersForTest   #用于导入测试数据
from db_fixture.test_data import test_data_arr

def create_user_test(url,payload,session):
    r = session.post(url=url,json=payload)
    return r

def delete_users(username,password):   #######创建用户后默认了该用户登录，该功能待确认
    '''用于创建用户后删除用户，保证测试数据库不被污染'''
    session = requests.Session()
    r1 = session.post('https://zlab.zlgcloud.com:443/v1/auth/login', json={"username": username, "password": password})
    r2 = session.delete('https://zlab.zlgcloud.com:443/v1/users/' + username)

class UsersCreateTest(unittest.TestCase):
    '''创建新用户测试'''

    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/users"
    def tearDown(self):
        print(self.result)
    def test_users_create_full(self):  ###已调试，可用
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入符合规则的未注册过的username、password、mobile、email和获取的验证码'''
        user = UsersForTest(13)
        r = user.create_users(isagent=False)
        print('response',r.json())
        self.result = r.status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,201)
    def test_users_create_full_agent(self):
        '''创建代理商'''
        user = UsersForTest(13)
        self.result = user.create_users(isagent=True).status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,201)
    def test_users_create_mobile_duplicate(self):
        '''用已注册过的手机号进行注册'''
        user = UsersForTest(13)
        user.create_users()
        user1 = UsersForTest(14)
        user1.mobile = user.mobile
        self.result = user1.create_users().status_code
        user.login()
        user.delete_users()
        user1.login()
        user1.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_smscode_null(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入符合规则的未注册过的username、password、mobile、email和获取的验证码为空'''
        user = UsersForTest(13)
        self.result = requests.post(url=self.base_url,json={"username":user.username,"password":user.password,"mobile":user.password,"smscode":""}).status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_smscode_5(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码， 然后传入符合规则的未注册过的username、password、mobile、email和获取的验证码前5位'''
        session = requests.Session()
        user = UsersForTest(13,session=session)
        smscode = user.get_smscode(mobile=user.mobile).json()['message']
        self.result = session.post(url=self.base_url,json={"username":user.username,"password":user.password,"mobile":user.password,"smscode":smscode[:-1]}).status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_smscode_double_1(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号先后获取两个验证码，然后传入符合规则的未注册过的username、password、mobile、email和获取的第一个验证码'''
        session = requests.Session()
        user = UsersForTest(13)
        smscode1 = user.get_smscode(mobile=user.mobile).json()['message']
        smscode2 = user.get_smscode(mobile=user.mobile).json()['message']
        self.result = session.post(url=self.base_url,json={"username":user.username,"password":user.password,"mobile":user.mobile,"smscode":smscode1}).status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)
    def test_users_create_smscode_2(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号先后获取两个验证码，然后传入符合规则的未注册过的username、password、mobile、email和获取的第二个验证码'''
        session = requests.Session()
        user = UsersForTest(13,session=session)
        smscode1 = user.get_smscode(mobile=user.mobile).json()['message']
        time.sleep(1)
        smscode2 = user.get_smscode(mobile=user.mobile).json()['message']
        self.result = session.post(url=self.base_url,json={"username":user.username,"password":user.password,"mobile":user.mobile,"smscode":smscode2,"email":user.email}).status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,201)
    def test_users_create_username_duplicate(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入已注册过的username和一个常规的password、mobile、email和获取的验证码'''
        user1 = UsersForTest(13)
        user1.create_users()
        user2 = UsersForTest(14)
        user2.username = user1.username
        self.result = user2.create_users().status_code
        user1.login()
        user1.delete_users()
        user2.login()
        user2.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_username_null(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入空的username和一个常规的password、mobile、email和获取的验证码'''
        user = UsersForTest(13)
        user.username = ""
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_username_1(self):  ###已调试，可用
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入少于2个字符的username和一个常规的password、mobile、email和获取的验证码'''
        user = UsersForTest(13)
        user.username = 'a'
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_username_2(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码， 然后传入等于2个字符的username和一个常规的password、mobile、email和获取的验证码'''
        user = UsersForTest(13)
        user.username = 'ab'
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,201)

    def test_users_create_username_64(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入等于32位字符的username和一个常规的password、mobile、email和获取的验证码'''
        user = UsersForTest(13)
        user.username = '0123456789012345678901234567890120123456789012345678901234567890'
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,201)

    def test_users_create_username_65(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入多于32位字符的username和一个常规的password、mobile、email和获取的验证码'''
        user = UsersForTest(13)
        user.username = '01234567890123456789012345678901201234567890123456789012345678901'
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)
    def test_users_create_password_null(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、mobile、email、获取的验证码和空的password'''
        user = UsersForTest(13)
        user.password = ""
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_password_8(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、mobile、email、获取的验证码和等于8位字符的password'''
        user = UsersForTest(13)
        user.password = "12345678"
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,201)

    def test_users_create_password_16(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、mobile、email、获取的验证码和等于16位字符的password'''
        user = UsersForTest(13)
        user.password = "1234567812345678"
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,201)

    def test_users_create_password_7(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、mobile、email、获取的验证码和少于8位字符的password'''
        user = UsersForTest(13)
        user.password = "1234567"
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_password_17(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、mobile、email、获取的验证码和多于16位字符的password'''
        user = UsersForTest(13)
        user.password = "12345678123456781"
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_mobile_null(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、password、email、获取的验证码和空的手机号'''
        session = requests.Session()
        user = UsersForTest(13,session=session)
        smscode = user.get_smscode(mobile=user.mobile).json()['message']
        self.result = session.post(url=self.base_url,json={"username":user.username,"password":user.password,"mobile":"","smscode":smscode}).status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_mobile_10(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、password、email、获取的验证码和少于11位的手机号'''
        session = requests.Session()
        user = UsersForTest(13,session=session)
        smscode = user.get_smscode(mobile=user.mobile).json()['message']
        self.result = session.post(url=self.base_url,json={"username":user.username,"password":user.password,"mobile":user.mobile[:-1],"smscode":smscode}).status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_mobile_exist(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、password、email、获取的验证码和其他未注册过的mobile'''
        user1 = UsersForTest(13)
        user1.create_users()
        user2 = UsersForTest(14)
        user2.mobile = user1.mobile
        self.result = user2.create_users().status_code
        user1.login()
        user1.delete_users()
        user2.login()
        user2.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_email_exist(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、password、mobile、获取的验证码和已注册过的email'''
        user1 = UsersForTest(13)
        user1.create_users()
        user2 = UsersForTest(14)
        user2.email = user1.email
        self.result = user2.create_users().status_code
        user1.login()
        user1.delete_users()
        user2.login()
        user2.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_email_nonstandard_1(self):
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、password、mobile、获取的验证码和不符合规则的email，xxxx'''
        user = UsersForTest(14)
        user.email = 'test12345600'
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_email_nonstandard_2(self):  ###已调试，可用
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、password、mobile、获取的验证码和不符合规则的email，xxxx@'''
        user = UsersForTest(14)
        user.email = 'test12345600@'
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_email_nonstandard_3(self):  ###已调试，可用
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、password、mobile、获取的验证码和不符合规则的email，xxxx@mail'''
        user = UsersForTest(14)
        user.email = 'test12345600@zlg'
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_email_nonstandard_4(self):  ###已调试，可用
        '''先在获取验证码的接口传入一个存在的未注册过的手机号获取验证码，然后传入常规的username、password、mobile、获取的验证码和不符合规则的email，xxxx@mail.'''
        user = UsersForTest(14)
        user.email = 'test12345600@zlg.'
        self.result = user.create_users().status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_mobile_1_smscode_1(self):
        '''先在获取验证码的接口先后传入两个未注册过的手机号，获得两个验证码，然后传入常规的username、password、email、第一个手机号和第二个验证码'''
        session = requests.Session()
        user1 = UsersForTest(num=13,session=session)
        smscode1 = user1.get_smscode(mobile=user1.mobile).json()['message']
        user2 = UsersForTest(num=14,session=session)
        smscode2 = user2.get_smscode(mobile=user2.mobile).json()['message']
        self.result = session.post(url=self.base_url,json={"username":user1.username,"password":user1.password,"mobile":user1.mobile,"smscode":smscode1}).status_code
        user1.login()
        user1.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_mobile_1_smscode_2(self):  ###已调试，可用
        '''先在获取验证码的接口先后传入两个未注册过的手机号，获得两个验证码，然后传入常规的username、password、email、第一个手机号和第一个验证码'''
        session = requests.Session()
        user1 = UsersForTest(num=13,session=session)
        smscode1 = user1.get_smscode(mobile=user1.mobile).json()['message']
        user2 = UsersForTest(num=14,session=session)
        smscode2 = user2.get_smscode(mobile=user2.mobile).json()['message']
        self.result = session.post(url=self.base_url,json={"username":user1.username,"password":user1.password,"mobile":user1.mobile,"smscode":smscode2}).status_code
        user1.login()
        user1.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_mobile_2_smscode_1(self):
        '''先在获取验证码的接口先后传入两个未注册过的手机号，获得两个验证码，然后传入常规的username、password、email、第二个手机号和第一个验证码'''
        session = requests.Session()
        user1 = UsersForTest(num=13,session=session)
        smscode1 = user1.get_smscode(mobile=user1.mobile).json()['message']
        user2 = UsersForTest(num=14,session=session)
        smscode2 = user2.get_smscode(mobile=user2.mobile).json()['message']
        self.result = session.post(url=self.base_url,json={"username":user2.username,"password":user2.password,"mobile":user2.mobile,"smscode":smscode1}).status_code
        user1.login()
        user1.delete_users()
        self.assertEqual(self.result,400)

    def test_users_create_mobile_smscode_4(self):  ###已调试，可用
        '''先在获取验证码的接口先后传入两个未注册过的手机号，获得两个验证码，然后传入常规的username、password、email、第二个手机号和第二个验证码'''
        session = requests.Session()
        user1 = UsersForTest(num=13,session=session)
        smscode1 = user1.get_smscode(mobile=user1.mobile).json()['message']
        user2 = UsersForTest(num=14,session=session)
        smscode2 = user2.get_smscode(mobile=user2.mobile).json()['message']
        self.result = session.post(url=self.base_url,json={"username":user2.username,"password":user2.password,"mobile":user2.mobile,"smscode":smscode2}).status_code
        user1.login()
        user1.delete_users()
        self.assertEqual(self.result,201)

    def test_users_create_failed(self):
        '''测试注册失败时，mobile是否被释放'''
        user = UsersForTest(13)
        user.password = '1234566'
        user.create_users()
        self.result = user.mobile_exist(user.mobile).status_code
        user.login()
        user.delete_users()
        self.assertEqual(self.result,404)
    def test_users_create_role_0(self):
        '''普通用户＝０'''
        user = UsersForTest(13)
        r = user.create_users()
        print(r.json())
        self.result = r.json()['data']['role']
        user.login()
        user.delete_users()
        self.assertEqual(self.result,0)
    def test_users_create_role_1(self):
        '''普通用户＝1'''
        user = UsersForTest(13)
        r = user.create_users(isagent=True)
        print(r.json())
        self.result = r.json()['data']['role']
        user.login()
        user.delete_users()
        self.assertEqual(self.result,1)

if __name__ == '__main__':
    user = UsersForTest(13)
    user.login()
    user.delete_users()
    unittest.main()
