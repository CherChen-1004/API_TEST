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
            500  服务器错误'''
def change_email_verify_code(new_email,session):  ##更新信息，不能修改密码、修改密码操作后不能用新密码登录
    '''创建获取修改邮箱的验证码函数'''
    r = session.get("https://zlab.zlgcloud.com:443/v1/auth/change_email_verify_code?email="+new_email)
    return r.json()['message']
def change_mobile_verify_code(new_mobile,session):
    '''创建获取修改邮箱的验证码函数'''
    r = session.get("https://zlab.zlgcloud.com:443/v1/auth/change_mobile_verify_code?mobile=")
    return r.json()['message']

class UsersMessageUpdateTest(unittest.TestCase):
    '''更新用户信息测试 '''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com/v1/users/"
    def tearDown(self):
        print(self.result)

    def test_users_message_update_password_right(self):
        '''创建一个用户，用该用户登录，传入该用户的username、符合规则的password'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        new_password = '123456789'
        payload = {"password": new_password}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        if r.status_code == 200:
            user.password = new_password
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)


    def test_users_message_update_nickname_right(self):
        '''创建一个用户，用该用户登录，传入该用户的username、符合规则的nickname'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        nickname = 'abcdef'
        payload = {"nickname": nickname}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,200)
    def test_users_message_update_desc_right(self):
        '''创建一个用户，用该用户登录，传入该用户的username、符合规则的desc'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        desc = 'abcdef'
        payload = {"nickname": desc}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,200)

    def test_users_message_update_email_right(self):
        '''创建一个用户，用该用户登录，先在获取修改邮箱的验证码接口填入一个未注册的邮箱获取验证码，然后传入该用户的username、验证码和新的邮箱'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        user2 = UsersForTest(19)
        new_email = user2.email
        code = user.get_changing_email_code(email=new_email).json()['message']
        payload = {"email": new_email}
        base_url = self.base_url + user.username+'?code='+code
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,200)
    def test_users_message_update_mobile_right(self):
        '''创建一个用户，用该用户登录，先在获取修改手机号的验证码接口填入一个未注册的手机号获取验证码，然后传入该用户的username、验证码和新的手机号'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        user2 = UsersForTest(19)
        new_mobile = user2.mobile
        code = user.get_changing_mobile_code(new_mobile).json()['message']
        print(code)
        payload = {"mobile": new_mobile}
        base_url = self.base_url + user.username+'?code='+code
        r = session.put(base_url, json=payload)
        print(r.json())
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,200)

    def test_users_message_update_nickname_desc(self):
        '''创建一个用户，用该用户登录，传入该用户的username、符合规则的password、nickname和desc'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        nickname = 'abcdef'
        desc = 'abcdef'
        payload = {"nickname":nickname,"desc":desc}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,200)


    def test_users_message_update_mobile_nickname_desc(self):
        '''创建一个用户，用该用户登录，先在获取修改手机号的验证码接口填入一个未注册的手机号获取验证码，然后传入该用户的username、验证码、新的手机号和nickname、desc、password'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        new_mobile = '12399999990'
        nickname = 'abcdef'
        desc = "abcdef"
        code = change_mobile_verify_code(new_mobile,session)
        payload = {"mobile": new_mobile,"nickname":nickname,"desc":desc}
        base_url = self.base_url + user.username+'?code='+code
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)


    def test_users_message_update_email_nickname_desc(self):
        '''创建一个用户，用该用户登录，先在获取修改邮箱的验证码接口填入一个未注册的手机号获取验证码，然后传入该用户的username、验证码、新的email和nickname、desc'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        user2 = UsersForTest(19)
        new_email = user2.email
        nickname = 'abcdef'
        desc = "abcdef"
        code = user.get_changing_email_code(email=new_email).json()['message']
        payload = {"email": new_email,"nickname":nickname,"desc":desc}
        base_url = self.base_url + user.username+'?code='+code
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,200)

    def test_users_message_update_mobile_email(self):
        '''创建一个用户，用该用户登录，先在获取修改手机的验证码接口填入一个未注册的手机号获取验证码，然后传入该用户的username、验证码、新的email和nickname、desc、password、新的手机号'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        new_mobile = '12399999990'
        new_email = 'test99999990@zlg.cn'
        nickname = 'abcdef'
        desc = "abcdef"
        new_password = '123456789'
        code = change_mobile_verify_code(new_mobile,session)
        payload = {"email": new_email,"mobile":new_mobile,"nickname":nickname,"desc":desc,"password":new_password}
        base_url = self.base_url + user.username+'?code='+code
        r = session.put(base_url, json=payload)
        if r.status_code == 200:
            user.password = new_password
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_users_message_update_(self):
        '''创建一个用户，用该用户登录，先在获取修改邮箱的验证码接口填入一个未注册的手机号获取验证码，然后传入该用户的username、验证码、新的email和nickname、desc、password'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        new_mobile = '12399999990'
        new_email = 'test99999990@zlg.cn'
        nickname = 'abcdef'
        desc = "abcdef"
        new_password = '123456789'
        code = change_email_verify_code(new_email,session)
        payload = {"email": new_email,"mobile":new_mobile,"nickname":nickname,"desc":desc,"password":new_password}
        base_url = self.base_url + user.username+'?code='+code
        r = session.put(base_url, json=payload)
        if r.status_code == 200:
            user.password = new_password
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_users_message_update_password_null(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username、空的password'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        new_password = ''
        payload = {"password":new_password}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        if r.status_code == 200:
            user.password = new_password
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_users_message_update_password_7(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username、少于8位字符的密码'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        new_password = '1234567'
        payload = {"password":new_password}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        if r.status_code == 200:
            user.password = new_password
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_users_message_update_password_8(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username、等于8位字符的密码'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        new_password = '1234567'
        payload = {"password":new_password}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        if r.status_code == 200:
            user.password = new_password
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_users_message_update_password_16(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username、等于16位字符的密码'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        new_password = '0123456789012345'
        payload = {"password":new_password}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        if r.status_code == 200:
            user.password = new_password
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_users_message_update_password_17(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username、多于16位字符的密码'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        new_password = '0123456789012345'
        payload = {"password":new_password}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        if r.status_code == 200:
            user.password = new_password
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_users_message_update_nickname_null(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username、空的nickname'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        nickname = ''
        payload = {"nickname":nickname}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)
    def test_users_message_update_nickname_1(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username、少于2位字符的nickname'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        nickname = 'a'
        payload = {"nickname":nickname}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_users_message_update_nickname_2(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username、等于2位字符的nickname'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        nickname = '*7'
        payload = {"nickname":nickname}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,200)
    def test_users_message_update_nickname_64(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username、等于32位字符的nickname'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        nickname = '*'*64
        payload = {"nickname":nickname}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,200)
    def test_users_message_update_nickname_65(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username、多于32位字符的nickname'''
        session = requests.Session()
        user = UsersForTest(18, session)
        user.create_users()
        user.login()
        nickname = '2'*65
        payload = {"nickname":nickname}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_users_message_update_mobile_exist(self):
        '''创建一个用户，用该用户登录，先在获取修改手机号的验证码接口填入一个已注册的手机号获取验证码，然后传入该用户的username、验证码和对应的手机号'''
        session1 = requests.Session()
        user1 = UsersForTest(18, session1)
        user1.create_users()
        session = requests.Session()
        user = UsersForTest(19,session)
        user.create_users()
        user.login()
        new_mobile = user1.mobile
        payload = {"mobile":new_mobile}
        code = change_mobile_verify_code(new_mobile,session)
        base_url = self.base_url + user.username+"?code="+code
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)

    def test_users_message_update_email_exist(self):
        '''创建一个用户，用该用户登录，先在获取修改邮箱的验证码接口填入一个已注册的手机号获取验证码，然后传入该用户的username、验证码和新的邮箱'''
        session1 = requests.Session()
        user1 = UsersForTest(18, session1)
        user1.create_users()
        session = requests.Session()
        user = UsersForTest(19,session)
        user.create_users()
        user.login()
        new_email = user1.email
        payload = {"email":new_email}
        code = change_email_verify_code(new_email,session)
        base_url = self.base_url + user.username+"?code="+code
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,400)
    def test_users_message_update_not_login(self):
        '''创建一个用户，不登陆，直接传入username和符合规则的nickname'''
        session = requests.Session()
        user = UsersForTest(18,session)
        user.create_users()
        # user.login()
        nickname = 'abcde'
        payload = {"nickname":nickname}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,401)

    def test_users_message_update_logout(self):
        '''创建一个用户，用该用户登录，退出，然后传入该用户的username，和更新password'''
        session = requests.Session()
        user = UsersForTest(18,session)
        user.create_users()
        user.login()
        r1 = session.get("https://zlab.zlgcloud.com:443/v1/auth/logout")
        new_password = '1234****____'
        payload = {"new_password":new_password}
        base_url = self.base_url + user.username
        r = session.put(base_url, json=payload)
        if r.status_code == 200:
            user.password = new_password
        user.login()
        user.delete_users()
        self.result = r.status_code
        self.assertEqual(self.result,401)

if __name__ == '__main__':
    unittest.main()
