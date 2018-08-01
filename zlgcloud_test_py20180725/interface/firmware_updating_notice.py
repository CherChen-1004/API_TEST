# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.test_data import models_list
'''返回码如下：
            200 操作成功
            400 无效参数
            401	没有登录
            403	没有权限
            404	固件不存在
            500	服务内部错误'''
def firmware_updating_notice_test(url,user_login,model,version,filter,login_or_not=1):
    '''参数化编程，login_user：登录的账号，model、version、file:传入的参数，login_or_not：1：登录，0：不登录，2：登录后再退出'''
    if filter == "":
        base_url = url + model + '/' + version + '/notify'
    else:
        base_url = url + model + '/' + version + '/notify?filter=' + filter
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
    return r.status_code

class FirmwareDeleteTest(unittest.TestCase):
    '''通知设备有新的固件 接口测试
    每条用例执行前提条件：创建两个普通用户，创建多个'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com/v1/firmware/"
        self.TestData = InitialData(92,92,92,94)
        self.users_arr = self.TestData.users_for_firmware_test(1)
        self.firmware_admin = self.users_arr[0]
        self.ordinary_users = self.users_arr[1]
        self.firmware_arr = self.TestData.upload_firmwares(3)
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_firmware()
        self.TestData.delete_all_users()
    def test_firmware_updating_notice_demo01_version_1(self):
        '''登录固件管理员，传入model=demo01，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[0],'1.01',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo01_version_2(self):
        '''登录固件管理员，传入model=demo01，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[0],'1.02',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo01_version_3(self):
        '''登录固件管理员，传入model=demo01，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[0],'1.03',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo02_version_1(self):
        '''登录固件管理员，传入model=demo02，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[1],'1.01',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo02_version_2(self):
        '''登录固件管理员，传入model=demo02，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[1],'1.02',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo02_version_3(self):
        '''登录固件管理员，传入model=demo02，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[1],'1.03',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo03_version_1(self):
        '''登录固件管理员，传入model=demo03，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[2],'1.01',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo03_version_2(self):
        '''登录固件管理员，传入model=demo03，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[2],'1.02',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo03_version_3(self):
        '''登录固件管理员，传入model=demo03，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[2],'1.03',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo04_version_1(self):
        '''登录固件管理员，传入model=demo04，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[3],'1.01',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo04_version_2(self):
        '''登录固件管理员，传入model=demo04，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[3],'1.02',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo04_version_3(self):
        '''登录固件管理员，传入model=demo04，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[3],'1.03',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_CANDTU_200UWGR_version_1(self):
        '''登录固件管理员，传入model=CANDTU-200UWGR，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[4],'1.01',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_CANDTU_200UWGR_version_2(self):
        '''登录固件管理员，传入model=CANDTU-200UWGR，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[4],'1.02',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_CANDTU_200UWGR_version_3(self):
        '''登录固件管理员，传入model=CANDTU-200UWGR，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[4],'1.03',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_INV001_ZLG_version_1(self):
        '''登录固件管理员，传入model=INV001-ZLG，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[5],'1.01',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_INV001_ZLG_version_2(self):
        '''登录固件管理员，传入model=INV001-ZLG，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[5],'1.02',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_INV001_ZLG_version_3(self):
        '''登录固件管理员，传入model=INV001-ZLG，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[5],'1.03',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_WM6232PU_version_1(self):
        '''登录固件管理员，传入model=WM6232PU，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[6],'1.01',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_WM6232PU_version_2(self):
        '''登录固件管理员，传入model=WM6232PU，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[6],'1.02',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_WM6232PU_version_3(self):
        '''登录固件管理员，传入model=WM6232PU，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[6],'1.03',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo01_version_without_decimal(self):
        '''登录固件管理员，传入model=demo01，version=1'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[0],'1',"",1)
        self.assertEqual(self.result,404)
    def test_firmware_updating_notice_demo01_version_1_decimal(self):
        '''登录固件管理员，传入model=demo01，version=1.0'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[0],'1.0',"",1)
        self.assertEqual(self.result,404)
    def test_firmware_updating_notice_demo01_version_3_decimal(self):
        '''登录固件管理员，传入model=demo01，version=1.012'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[0],'1.011',"",1)
        self.assertEqual(self.result,200)
    def test_firmware_updating_notice_demo01_version_char(self):
        '''登录固件管理员，传入model=demo01，version=1.012'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[0],'asdg',"",1)
        self.assertEqual(self.result,400)
    def test_firmware_updating_notice_demo01_ls_1(self):
        '''登录固件管理员，传入model=demo0，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[0][:-1],'1.01',"",1)
        self.assertEqual(self.result,400)
    def test_firmware_updating_notice_demo02_ls_1(self):
        '''登录固件管理员，传入model=demo0，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[1][:-1],'1.01',"",1)
        self.assertEqual(self.result,400)
    def test_firmware_updating_notice_demo03_ls_1(self):
        '''登录固件管理员，传入model=demo0，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[2][:-1],'1.01',"",1)
        self.assertEqual(self.result,400)
    def test_firmware_updating_notice_demo04_ls_1(self):
        '''登录固件管理员，传入model=demo0，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[3][:-1],'1.01',"",1)
        self.assertEqual(self.result,400)
    def test_firmware_updating_notice_CANDTU_200UWGR_ls_1(self):
        '''登录固件管理员，传入model=CANDTU-200UWG，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[4][:-1],'1.01',"",1)
        self.assertEqual(self.result,404)
    def test_firmware_updating_notice_INV001_ZLG_ls_1(self):
        '''登录固件管理员，传入model=INV001-ZL，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[5][:-1],'1.01',"",1)
        self.assertEqual(self.result,400)
    def test_firmware_updating_notice_WM6232PU_ls_1(self):
        '''登录固件管理员，传入model=WM6232P，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[6][:-1],'1.01',"",1)
        self.assertEqual(self.result,400)
    def test_firmware_updating_notice_filter_(self):
        '''登录固件管理员，传入model=WM6232P，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[6][:-1],'1.01',"",1)
        self.assertEqual(self.result,400)

    def test_firmware_updating_notice_ordinary_user(self):   ##存在Bug
        '''登录普通用户，传入model=WM6232P，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.ordinary_users,models_list[6],'1.01',"",1)
        self.assertEqual(self.result,403)
    def test_firmware_updating_notice_not_login(self):
        '''不登录，传入model=WM6232PU，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[6],'1.01',"",0)
        self.assertEqual(self.result,401)
    def test_firmware_updating_notice_logout(self):
        '''登录后退出，传入model=WM6232PU，version=1.01'''
        self.result = firmware_updating_notice_test(self.base_url,self.firmware_admin,models_list[6],'1.01',"",2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    for n in range(92,94):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()