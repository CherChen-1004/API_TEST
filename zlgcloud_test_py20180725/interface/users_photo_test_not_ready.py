#coding=utf_8
#Author = Cher Chan

import unittest
import requests
import os
import json
from db_fixture.test_data import UsersForTest
from db_fixture import test_data
'''返回码如下：
            200  操作成功
            400  无效参数
            401  没有登录
            500  服务器错误'''

class UsersPhotoTest(unittest.TestCase):
    '''上传头像接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com/v1/users/"
        self.photo_path = test_data.test_data_path + "\\test_photos/"
    def tearDown(self):
        print(self.result)

    def test_users_photo_jpg_right(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username和一个符合要求的.jpg后缀图片文件'''
        session = requests.Session()
        user = UsersForTest(21,session)
        user1 = user.create_users()
        print(user1.json())
        user.login()
        base_url = self.base_url + user.username + '/avatar'
        payload = {'file':('test_1.jpg',open(self.photo_path+'test_1.jpg','rb'),'image/jpeg')}
        r = session.post(base_url, files = payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.delete_users()
    def test_users_photo_png_right(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username和一个符合要求的.png后缀图片文件'''
        session = requests.Session()
        user = UsersForTest(21,session)
        user.create_users()
        user.login()
        base_url = self.base_url + user.username + '/avatar'
        payload = {'file':('test_2.png',open(self.photo_path+'test_2.png','rb'),'image/png')}
        r = session.post(base_url, files = payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.delete_users()

    def test_users_photo_PNG_right(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username和一个符合要求的.PNG后缀图片文件'''
        session = requests.Session()
        user = UsersForTest(21,session)
        user.create_users()
        user.login()
        base_url = self.base_url + user.username + '/avatar'
        payload = {'file':('test_3.PNG',open(self.photo_path+'test_3.PNG','rb'),'image/PNG')}
        r = session.post(base_url, files = payload)
        self.result = r.status_code
        self.assertEqual(self.result,200)
        user.delete_users()
    def test_users_photo_txt_file(self):
        '''创建一个用户，用该用户登录，然后传入该用户的username和一个非图片文件'''
        session = requests.Session()
        user = UsersForTest(21,session)
        user.create_users()
        user.login()
        base_url = self.base_url + user.username + '/avatar'
        payload = {'file':open(self.photo_path+'test.txt','rb')}
        r = session.post(base_url, files = payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

    def test_users_photo_bigger(self):
        ''''''
        session = requests.Session()
        user = UsersForTest(21,session)
        user.create_users()
        user.login()
        base_url = self.base_url + user.username + '/avatar'
        payload = {'file':('test_4.jpg',open(self.photo_path+'test_4.jpg','rb'),'image/jpeg')}
        r = session.post(base_url, files = payload)
        self.result = r.status_code
        self.assertEqual(self.result,400)
        user.delete_users()

    def test_users_photo_username_wrong(self):
        '''创建一个用户，用该用户登录，然后传入非该用户的username和一个符合要求的.jpg后缀图片文件'''
        session = requests.Session()
        user = UsersForTest(21,session)
        user.create_users()
        user.login()
        base_url = self.base_url + '12399999999' + '/avatar'
        payload = {'file':('test_1.jpg',open(self.photo_path+'test_1.jpg','rb'),'image/jpeg')}
        r = session.post(base_url, files = payload)
        self.result = r.status_code
        self.assertEqual(self.result,403)
        user.delete_users()

    def test_users_photo_not_login(self):
        '''创建一个用户，不登录，然后传入该用户的username和一个符合要求的.jpg后缀图片文件'''
        session = requests.Session()
        user = UsersForTest(21,session)
        user.create_users()
        # user.login()
        base_url = self.base_url + user.username + '/avatar'
        payload = {'file':('test_1.jpg',open(self.photo_path+'test_1.jpg','rb'),'image/jpeg')}
        r = session.post(base_url, files = payload)
        self.result = r.status_code
        self.assertEqual(self.result,401)
        user.login()
        user.delete_users()
    def test_users_photo_logout(self):
        '''创建一个用户，用该用户登录，然后退出，然后传入该用户的username和一个符合要求的.jpg后缀图片文件'''
        session = requests.Session()
        user = UsersForTest(21,session)
        user.create_users()
        user.login()
        user.logout()
        base_url = self.base_url + user.username + '/avatar'
        payload = {'file':('test_1.jpg',open(self.photo_path+'test_1.jpg','rb'),'image/jpeg')}
        r = session.post(base_url, files = payload)
        self.result = r.status_code
        self.assertEqual(self.result,401)
        user.login()
        user.delete_users()

if __name__ == '__main__':
    user = UsersForTest(21)
    r = user.login()
    print(r.json())
    user.delete_users()
    unittest.main()
