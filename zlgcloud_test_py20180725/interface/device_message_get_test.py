# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData

'''返回码如下：
            200	操作成功
            401	没有登录
            403 没有权限
            500	服务器错误'''

def get_device_message_test(url,login_user,devtype,devid,login_or_not=1):
    '''参数化编程，login_user:登录的用户信息，login_or_not:是否登录，1：登录，0：不登录，2：登录后退出'''
    base_url = url + devid + '?devtype=' + devtype
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
    if r.status_code == 200:
        print(r.json())
        result = r.json()['devtype'] == devtype and r.json()['devid'] == devid
        return result
    else:
        return r.status_code

class DevicesMessageGetTest(unittest.TestCase):   #####与开发确认数据的取值范围
    '''返回设备信息接口查询 接口测试'''

    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/devices/"
        self.TestData = InitialData(77, 77, 77,79)
        self.users_device_groups_devices_arr = self.TestData.users_device_groups_devices(2,2)
        self.user_0 = self.users_device_groups_devices_arr[0]
        self.user_1 = self.users_device_groups_devices_arr[1]
        self.user_0_device_group_0 = self.user_0['device_groups'][0]
        self.user_0_device_group_1 = self.user_0['device_groups'][1]
        self.user_1_device_group_0 = self.user_1['device_groups'][0]
        self.user_1_device_group_1 = self.user_1['device_groups'][1]
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_devices_and_data()
        self.TestData.delete_all_agents_and_orgnizations()
        self.TestData.delete_all_users()
    def test_get_device_message_right(self):
        '''登录普通用户，传入改用户所包含设备的devtype和devid'''
        self.result = get_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,True)
    def test_get_device_message_devtype_ls_1(self):
        '''登录普通用户，传入改用户所包含设备的devtype少一位字符和devid'''
        self.result = get_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'][:-1],self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,400)
    def test_get_device_message_devtype_wrong(self):
        '''登录普通用户，传入改用户所包含设备的devid和错误的devtype'''
        self.result = get_device_message_test(self.base_url,self.user_0,'hsiduhg',self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,400)
    def test_get_device_message_devid_ls_1(self):
        '''登录普通用户，传入改用户所包含设备的devtype和devid少一位字符'''
        self.result = get_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'][:-1],1)
        self.assertEqual(self.result,404)
    def test_get_device_message_devid_wrong(self):
        '''登录普通用户，传入改用户所包含设备的devtype和不存在的devid'''
        self.result = get_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],"sdgisgfnv7r",1)
        self.assertEqual(self.result,404)
    def test_get_device_message_devid_of_other_user(self):
        '''登录普通用户，传入其他用户包含设备的devid'''
        self.result = get_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,403)
    def test_get_device_message_other_not_login(self):
        '''不登录，传入设备的devtype和devid'''
        self.result = get_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],0)
        self.assertEqual(self.result,401)
    def test_get_device_message_other_logout(self):
        '''登录某用户后退出，传入该用户所包含设备的devtype和devid'''
        self.result = get_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],2)
        self.assertEqual(self.result,401)
    def test_get_device_message_without_owner(self):
        '''登录某普通用户，传入无owner的设备的devtype和devid'''
        self.result = get_device_message_test(self.base_url,self.user_0,'inverter','test_1',1)
        self.assertEqual(self.result,404)

if __name__ == '__main__':
    unittest.main()

    