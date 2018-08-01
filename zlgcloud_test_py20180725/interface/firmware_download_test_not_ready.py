# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.test_data import models_list

'''返回码如下：
            200 操作成功
            400	无效参数
            401 没有登录
            403	没有权限
            500	服务器内部错误'''

class Initialize(object):
    '''创建初始化类'''
    def __init__(self,first_user_num=0,last_user_num=0,firmware_num=0):
        self.first_user_num = first_user_num
        self.last_user_num = last_user_num
        self.firware_num = firmware_num
        self.TestData = InitialData(first_user_num=first_user_num,last_user_num=last_user_num+1)
    def setup(self):
        '''创建2个普通用户，登录admin将其中1个角色置为固件管理员'''
        global users_list,firmware_list
        users_list = self.TestData.users_for_firmware_test(firmware_admin_num=1)
        firmware_list = self.TestData.upload_firmwares(firmware_num=self.firware_num)
        print(firmware_list)
    def teardown(self):
        '''登录固件管理员账号，删除所有测试中上传的固件，然后删除所有的用户'''
        global users_list
        self.TestData.delete_all_firmware(user_num=self.first_user_num)
        self.TestData.delete_all_users()

def download_firmware_list_test(url,user_login,model,version,login_or_not=1):
    '''参数化编程，login_user：登录的账号，model、version、file:传入的参数，login_or_not：1：登录，0：不登录，2：登录后再退出'''
    base_url = url + model + '/' + version
    session = requests.Session()
    user = UsersForTest(int(user_login['mobile'][-3:]),session)
    if login_or_not == 1:
        user.login()
        r = session.get(base_url)
    elif login_or_not == 0:
        r = requests.get(base_url)
    else:
        user.login()
        user.logout()
        r = session.get(base_url)
    return r.status_code

class FirmwareDownloadTest(unittest.TestCase):  ##运行前确保文件路径正确
    '''下载固件 接口测试'''
    @classmethod
    def setUpClass(cls):
        global Initial
        Initial = Initialize(first_user_num=526,last_user_num=527,firmware_num=3)
        Initial.setup()
    @classmethod
    def tearDownClass(cls):
        global Initial
        Initial.teardown()
    def setUp(self):
        global users_list,firmware_list
        self.base_url = "https://zlab.zlgcloud.com/v1/public/firmware/"
        self.firmware_admin = users_list[0]
        self.original_user = users_list[1]
        self.firmware_arr = firmware_list
    def tearDown(self):
        print(self.result)
    def test_download_firmware_firmware_admin_login_normal(self):
        '''登录固件管理员，传入model=demo01，version=1.01'''
        for model in models_list:
            with self.subTest():
                self.result = download_firmware_list_test(url=self.base_url,user_login=self.firmware_admin,model=model,version='1.01',login_or_not=1)
                print(self.result)
                self.assertEqual(self.result,200)
    def test_download_firmware_original_user_login_normal(self):
        '''登录固件管理员，传入model=demo01，version=1.01'''
        for model in models_list:
            with self.subTest():
                self.result = download_firmware_list_test(url=self.base_url,user_login=self.original_user,model=model,version='1.01',login_or_not=1)
                print(self.result)
                self.assertEqual(self.result,200)
    def test_download_firmware_demo01_version_without_decimal(self):
        '''登录固件管理员，传入model=demo01，version=1'''
        self.result = download_firmware_list_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='1',login_or_not=1)
        self.assertEqual(self.result,404)
    def test_download_firmware_demo01_version_1_decimal(self):
        '''登录固件管理员，传入model=demo01，version=1'''
        self.result = download_firmware_list_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='1.0',login_or_not=1)
        self.assertEqual(self.result,404)
    def test_download_firmware_demo01_version_3_decimal(self):
        '''登录固件管理员，传入model=demo01，version=1'''
        self.result = download_firmware_list_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='1.012',login_or_not=1)
        self.assertEqual(self.result,404)
    def test_download_firmware_model_wrong(self):
        '''登录固件管理员，分别传入少一个字符的model值'''
        for model in models_list:
            with self.subTest():
                self.result = download_firmware_list_test(url=self.base_url,user_login=self.firmware_admin,model=model[:-1],version='1.02',login_or_not=1)
                print(self.result)
                self.assertEqual(self.result,400)
    def test_download_firmware_not_login(self):
        '''登录固件管理员，传入model=demo01，version=1'''
        self.result = download_firmware_list_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='1.01',login_or_not=0)
        self.assertEqual(self.result,401)
    def test_download_firmware_logout(self):
        '''登录固件管理员，传入model=demo01，version=1'''
        self.result = download_firmware_list_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='1.01',login_or_not=2)
        self.assertEqual(self.result,401)

if __name__ == '__main__':
    unittest.main()
