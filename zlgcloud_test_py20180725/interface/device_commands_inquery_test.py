# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.test_data import device_event_test_data_arr

'''返回码如下：
            200 操作成功
            400	无效参数
            401	没有登录
            404 设备不存在'''
def get_device_commands(url,login_user,devtype,devid,login_or_not):
    '''查询设备支持的命令 接口测试
    每条用例前提条件：创建两个普通用户，每个用户添加1个设备分组，添加2个设备'''
    base_url = url + devid + "/commands?devtype=" + devtype
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.get(base_url)
    elif login_or_not == 0:
        r = requests.get(base_url)
    else:
        user.login()
        user.logout()
        r = session.get(base_url)
    return r

class DeviceCommandsInqueryTest(unittest.TestCase):
    '''查询设备支持的命令 接口测试
    每条用例前提条件：创建两个普通用户，每个用户添加三条devid不等、time不等的设备事件'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/devices/"
        self.TestData = InitialData(88,88,88,90)
        self.users_device_groups_devices = self.TestData.users_device_groups_devices(1,2)
        self.user_0 = self.users_device_groups_devices[0]
        self.user_1 = self.users_device_groups_devices[1]
        self.user_0_device_0 = self.user_0['device_groups'][0]['devices'][0]
        self.user_1_device_0 = self.user_1['device_groups'][0]['devices'][0]
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_devices_and_data()
        self.TestData.delete_all_users()
    def test_get_device_commands_right(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid'''
        self.result = get_device_commands(self.base_url,self.user_0,self.user_0_device_0['devtype'],self.user_0_device_0['devid'],1).status_code
        self.assertEqual(self.result,200)
    def test_get_device_commands_devtype_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devtype少一位字符'''
        self.result = get_device_commands(self.base_url,self.user_0,self.user_0_device_0['devtype'][:-1],self.user_0_device_0['devid'],1).status_code
        self.assertEqual(self.result,400)
    def test_get_device_commands_devtype_not_exist(self):
        '''登录普通用户，传入不存在的devtype'''
        self.result = get_device_commands(self.base_url,self.user_0,'rgersadgf',self.user_0_device_0['devid'],1).status_code
        self.assertEqual(self.result,400)
    # def test_get_device_commands_devid_ls_1(self):  ##不对devid进行检测
    #     '''登录普通用户，传入该用户所包含设备的devid少一位字符'''
    #     self.result = get_device_commands(self.base_url,self.user_0,self.user_0_device_0['devtype'],self.user_0_device_0['devid'][:-1],1).status_code
    #     self.assertEqual(self.result,400)
    # def test_get_device_commands_devid_not_exist(self):  ##不对devid进行检测
    #     '''登录普通用户，传入不存在的devid'''
    #     self.result = get_device_commands(self.base_url,self.user_0,self.user_0_device_0['devtype'],'sgrdfdsg))gt',1).status_code
    #     self.assertEqual(self.result,400)
    # def test_get_device_commands_devid_of_other_users(self):        ##不对devid进行检测
    #     '''登录普通用户，传入其他用户所包含设备的devid'''
    #     self.result = get_device_commands(self.base_url,self.user_0,self.user_0_device_0['devtype'],self.user_1_device_0['devid'],1).status_code
    #     self.assertEqual(self.result,403)
    def test_get_device_commands_devid_without_owner(self):
        '''登录普通用户，传入没有onwer的设备的devid'''
        self.result = get_device_commands(self.base_url,self.user_0,'inverter','test_1',1).status_code
        self.assertEqual(self.result,200)
    def test_get_device_commands_not_login(self):
        '''不登录，传入存在的设备的devid和devtype'''
        self.result = get_device_commands(self.base_url,self.user_0,self.user_0_device_0['devtype'],self.user_0_device_0['devid'],0).status_code
        self.assertEqual(self.result,401)
    def test_get_device_commands_logout(self):
        '''登录后退出，传入存在的设备的devid和devtype'''
        self.result = get_device_commands(self.base_url,self.user_0,self.user_0_device_0['devtype'],self.user_0_device_0['devid'],2).status_code
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    unittest.main()

