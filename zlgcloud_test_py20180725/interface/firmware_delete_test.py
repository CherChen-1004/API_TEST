# coding=utf_8
# Author=Cher Chan

'''返回码如下：
            200 操作成功
            400	无效参数
            401 没有登录
            403	没有权限
            500	服务器内部错误'''

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.test_data import models_list
# models_list = ["demo01","demo02", "demo03","demo04","CANDTU-200UWGR","WM6232PU","temp01","temp02","temp03"]

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

def delete_firmware_list_test(url,user_login,model,version,login_or_not=1):
    '''参数化编程，login_user：登录的账号，model、version、file:传入的参数，login_or_not：1：登录，0：不登录，2：登录后再退出'''
    base_url = url + model + '/' + version
    session = requests.Session()
    user = UsersForTest(int(user_login['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.delete(base_url)
    elif login_or_not == 0:
        r = requests.delete(base_url)
    else:
        user.login()
        user.logout()
        r = session.delete(base_url)

    if r.status_code == 200:
        r1 = session.get("https://zlab.zlgcloud.com/v1/firmware/"+model)
        if r1.status_code == 200:
            # print(r1.json())
            firmware_arr = r1.json()
            version_arr = []
            for firmware in firmware_arr:
                version_arr.append(firmware['name'])
            version_arr.sort(key=str)
            return version_arr
        else:
            print('Get firmware list failed!')
    else:
        return r.status_code

    print(r.json())
    return r.status_code

class FirmwareDeleteTest(unittest.TestCase):  ##运行前确保文件路径正确
    '''删除固件 接口测试'''
    @classmethod
    def setUpClass(cls):
        global Initial
        Initial = Initialize(first_user_num=92,last_user_num=93,firmware_num=3)
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
    def test_delete_firmware_a_normal(self):
        '''登录固件管理员，传入各个model值的正常测试'''
        for model in models_list:
            with self.subTest():
                self.result = delete_firmware_list_test(url=self.base_url,user_login=self.firmware_admin,model=model,version='1.01',login_or_not=1)
                print(self.result)
                self.assertEqual(self.result,['1.02', '1.03'])
    def test_delete_firmware_demo01_version_without_decimal(self):
        '''登录固件管理员，传入model=demo01，version=1'''
        self.result = delete_firmware_list_test(self.base_url,self.firmware_admin,'demo01','1',1)
        self.assertEqual(self.result,404)
    def test_delete_firmware_demo01_version_1_decimal(self):
        '''登录固件管理员，传入model=demo01，version=1.0'''
        self.result = delete_firmware_list_test(self.base_url,self.firmware_admin,'demo01','1.0',1)
        self.assertEqual(self.result,404)
    def test_delete_firmware_demo01_version_3_decimal(self):
        '''登录固件管理员，传入model=demo01，version=1.012'''
        self.result = delete_firmware_list_test(self.base_url,self.firmware_admin,'demo01','1.021',1)
        self.assertEqual(self.result,[ '1.03'])
    def test_delete_firmware_ordinary_user(self):
        '''登录普通用户'''
        self.result = delete_firmware_list_test(self.base_url,self.original_user,'demo02','1.02',1)
        self.assertEqual(self.result,403)
    def test_delete_firmware_not_login(self):
        '''不登录'''
        self.result = delete_firmware_list_test(self.base_url,self.firmware_admin,'dem03','1.01',0)
        self.assertEqual(self.result,401)
    def test_delete_firmware_logout(self):
        '''登录后退出'''
        self.result = delete_firmware_list_test(self.base_url,self.firmware_admin,'demo4','1.01',2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    for n in range(88,93):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()
