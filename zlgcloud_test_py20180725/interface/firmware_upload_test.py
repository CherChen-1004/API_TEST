# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.test_data import test_data_path
models_list = ["demo01","demo02", "demo03","demo04","CANDTU-200UWGR","WM6232PU","temp01","temp02","temp03"]

'''返回码如下：
            200 操作成功
            400	无效参数
            401 没有登录
            500 服务器内部错误'''
class Initialize(object):
    '''创建初始化类'''
    def __init__(self,first_user_num,last_user_num):
        self.first_user_num = first_user_num
        self.last_user_num = last_user_num
        self.TestData = InitialData(first_user_num=first_user_num,last_user_num=last_user_num+1)
    def setup(self):
        '''创建2个普通用户，登录admin将其中1个角色置为固件管理员'''
        global users_list
        users_list = self.TestData.create_users()
        session = requests.Session()
        admin = UsersForTest(num=0,session=session)
        admin.username = "admin"
        admin.password = "admin123"
        admin.login()
        r1 = admin.update_user_message(username=users_list[0]['username'],payload={"role":2})
        print('Set the firmware admin',r1.status_code)
    def teardown(self):
        '''登录固件管理员账号，删除所有测试中上传的固件，然后删除所有的用户'''
        global users_list
        self.TestData.delete_all_firmware(user_num=self.first_user_num)
        self.TestData.delete_all_users()

def upload_firmware_test(url,user_login,model,version,file,login_or_not=1):
    '''参数化编程，login_user：登录的账号，model、version、file:传入的参数，login_or_not：1：登录，0：不登录，2：登录后再退出'''
    base_url = url + model + '/' + version
    session = requests.Session()
    user = UsersForTest(int(user_login['mobile'][-2:]),session)
    file_path = test_data_path + "\\test_firmware/"
    payload = {'file': (file, open(file_path + file, 'rb'))}
    if login_or_not == 1:
        user.login()
        r = session.post(base_url,files=payload)
    elif login_or_not == 0:
        r = requests.post(base_url,files=payload)
    else:
        user.login()
        user.logout()
        r = session.post(base_url,files=payload)
    return r

class FirmwareUploadTest(unittest.TestCase):  ##运行前确保文件路径正确
    '''上传固件 接口测试'''
    @classmethod
    def setUpClass(cls):
        global Initial
        Initial = Initialize(94,96)
        Initial.setup()
    @classmethod
    def tearDownClass(cls):
        global  Initial
        Initial.teardown()
    def setUp(self):
        global users_list
        self.base_url = "https://zlab.zlgcloud.com/v1/firmware/"
        self.firmware_admin = users_list[0]
        self.original_user = users_list[1]

    def tearDown(self):
        print(self.result)
    def test_upload_firware_normal(self):
        '''登录固件管理用户，分别传入models_list = ["demo01","demo02", "demo03","demo04","CANDTU-200UWGR","WM6232PU","temp01","temp02","temp03"]，verion均为1.00，file大小为2M左右'''
        for model in models_list:
            with self.subTest():
                self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model=model,version='1.00',file='firmware_test_2M.dll',login_or_not=1).status_code
                print(self.result)
                self.assertEqual(self.result,200)
    def test_upload_firmware_version_char(self):
        '''登录固件管理员用户，传入model=CANDTU-200UWGR,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='df',file='firmware_test_2M.dll',login_or_not=1).status_code
        self.assertEqual(self.result,400)
    def test_upload_firmware_version_decimal_place_3(self):
        '''登录固件管理员用户，传入model=CANDTU-200UWGR,version=3.123, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='3.123',file='firmware_test_2M.dll',login_or_not=1).json()['data']['name']
        self.assertEqual(self.result,'3.12')
    def test_upload_firmware_version_decimal_place_1(self):
        '''登录固件管理员用户，传入model=CANDTU-200UWGR,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='3.1',file='firmware_test_2M.dll',login_or_not=1).json()['data']['name']
        self.assertEqual(self.result,'3.10')
    def test_upload_firmware_version_decimal_place_char(self):
        '''登录固件管理员用户,传入model=CANDTU-200UWGR,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='3.df',file='firmware_test_2M.dll',login_or_not=1).status_code
        self.assertEqual(self.result,400)
    def test_upload_firmware_version_special_char(self):
        '''登录固件管理员用户,传入model=CANDTU-200UWGR,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='&&',file='firmware_test_2M.dll',login_or_not=1).status_code
        self.assertEqual(self.result,400)
    def test_upload_firmware_file_5M(self):
        '''登录固件管理员用户,传入model=WM6232PU,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model='demo01',version='1.00',file='firmware_test_5.6M.txt',login_or_not=1).status_code
        self.assertEqual(self.result,200)
    def test_upload_firmware_file_9M(self):
        '''登录固件管理员用户,传入model=WM6232PU,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model = 'demo01',version='1.00',file='firmware_test9.72M.zip',login_or_not=1).status_code
        self.assertEqual(self.result,200)
    def test_upload_firmware_file_10M(self):
        '''登录固件管理员用户,传入model=WM6232PU,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model = 'demo01',version='1.00',file='firware_test_10.6M.zip',login_or_not=1).status_code
        self.assertEqual(self.result,400)
    def test_upload_firmware_file_56K(self):
        '''登录固件管理员用户,传入model=WM6232PU,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model = 'demo01',version='1.00',file='firware_test_58k.txt',login_or_not=1).status_code
        self.assertEqual(self.result,200)
    def test_upload_firmware_ordinary_login(self):
        '''登录普通用户,传入model=WM6232PU,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.original_user,model = 'demo01',version='1.00',file='firware_test_58k.txt',login_or_not=1).status_code
        self.assertEqual(self.result,403)
    def test_upload_firmware_not_login(self):
        '''不登录,传入model=CANDTU-200UWGR,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model = 'demo01',version='1.00',file='firmware_test_2M.dll',login_or_not=0).status_code
        self.assertEqual(self.result,401)
    def test_upload_firmware_logout(self):
        '''不登录，传入model=CANDTU-200UWGR,version1.00, file文件大小为2M左右'''
        self.result = upload_firmware_test(url=self.base_url,user_login=self.firmware_admin,model = 'demo01',version='1.00',file='firmware_test_2M.dll',login_or_not=2).status_code
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    unittest.main()
