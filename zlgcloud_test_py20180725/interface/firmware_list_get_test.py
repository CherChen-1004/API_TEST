# coding=utf_8
# Author=Cher Chan
# 下载固件接口会重新创建
import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.test_data import models_list
'''返回码如下：
            200 操作成功
            400	无效参数
            401 没有登录
            500 服务器内部错误'''
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

def get_firmware_list_test(url,user_login,model,login_or_not=1):
    '''参数化编程，login_user：登录的账号，model、version、file:传入的参数，login_or_not：1：登录，0：不登录，2：登录后再退出'''
    base_url = url + model
    session = requests.Session()
    user = UsersForTest(int(user_login['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.get(base_url)
    elif login_or_not == 0:
        r = requests.get(base_url)
    else:
        user.login()
        user.logout()
        r = session.get(base_url)
    if r.status_code == 200:
        firmware_arr = r.json()
        version_arr = []
        for firmware in firmware_arr:
            version_arr.append(firmware['name'])
        version_arr.sort(key=str)
        return version_arr
    else:
        return r.status_code
class FirmwareGetTest(unittest.TestCase):  ##运行前确保文件路径正确
    '''获取固件列表 接口测试'''
    @classmethod
    def setUpClass(cls):
        global Initial
        Initial = Initialize(first_user_num=92,last_user_num=94,firmware_num=3)
        Initial.setup()
    @classmethod
    def tearDownClass(cls):
        global Initial
        Initial.teardown()
    def setUp(self):
        global users_list,firmware_list
        self.base_url = "https://zlab.zlgcloud.com/v1/firmware/"
        self.firmware_admin = users_list[0]
        self.original_user = users_list[1]
        self.firmware_arr = firmware_list
    def tearDown(self):
        print(self.result)
    def test_get_firmware_list_normal(self):
        '''登录固件管理员，逐个填入正确model值'''
        for model in models_list:
            with self.subTest():
                self.result = get_firmware_list_test(url=self.base_url,user_login=self.firmware_admin,model=model,login_or_not=1)
                print(self.result)
                self.assertEqual(self.result,['1.01','1.02','1.03'])
    # def test_get_firmware_list_model_less_1(self):
    #     '''登录固件管理员，model少一个字符'''
    #     for model in models_list:
    #         with self.subTest():
    #             self.result = get_firmware_list_test(url=self.base_url,user_login=self.firmware_admin,model=model[:-1],login_or_not=1)
    #             print(self.result)
    #             self.assertEqual(self.result,400)
    def test_get_firmware_list_ordinary_login(self):
        '''登录普通用户，传入model=demo01'''
        self.result = get_firmware_list_test(self.base_url, self.original_user, 'demo01', 1)
        self.assertEqual(self.result, 403)
    def test_get_firmware_list_not_login(self):
        '''不登录'''
        self.result = get_firmware_list_test(self.base_url, self.firmware_admin, 'demo01', 0)
        self.assertEqual(self.result, 401)
    def test_get_firmware_list_logout(self):
        '''登录后退出'''
        self.result = get_firmware_list_test(self.base_url, self.firmware_admin, 'demo01', 2)
        self.assertEqual(self.result, 401)
if __name__ == '__main__':
    for n in range(92,94):
        user = UsersForTest(n)
        r1 = user.login()
        print(r1.json())
        r2 = user.delete_users()
        print(r2.json())
    unittest.main()
