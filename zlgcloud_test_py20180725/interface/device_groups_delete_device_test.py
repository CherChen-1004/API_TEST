# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData

'''返回码如下：
            200	操作成功
            401	没有登录
            404 设备分组不存在
            500	服务器错误'''

def delete_device_test(url, login_user, groupid, devtype,devid, login_or_not=1):
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]), session)
    base_url = url + groupid + '/'+ devid +'?'+ 'devtype='+devtype
    if login_or_not == 1:
        user.login()
        r = session.delete(base_url)
    elif login_or_not == 0:
        r = requests.delete(base_url)
    else:
        user.login()
        user.logout()
        r = session.delete(base_url)
    return r.status_code


class DeviceGroupsAddDeviceTest(unittest.TestCase):
    '''从设备分组中删除设备 接口测试
    用例前提条件：创建两个普通用户，每个用户创建两个设备分组，每个分组添加两个设备'''

    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/device_groups/"
        self.TestData = InitialData(53, 53, 53,55)
        self.users_device_groups_devices_arr = self.TestData.users_device_groups_devices(2,2)
        self.user_0 = self.users_device_groups_devices_arr[0]
        self.user_1 = self.users_device_groups_devices_arr[1]
        self.user_0_device_group_0 = self.user_0['device_groups'][0]
        self.user_0_device_group_1 = self.user_0['device_groups'][1]
        self.user_1_device_group_0 = self.user_1['device_groups'][0]

    def tearDown(self):
        print(self.result)
        # self.TestData.delete_all_agents_and_orgnizations()
        self.TestData.delete_all_users()
    def test_device_groups_delete_device_right(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，devtype和devid为对应设备分组包含的设备'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'],self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,200)
    def test_device_groups_delete_groupid_23(self):
        '''登录普通用户，传入groupid为该用户包含的groupid前23位，devtype和devid为对应设备分组包含的设备'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'][:-1],self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,400)
    def test_device_groups_delete_groupid_23_2(self):
        '''登录普通用户，传入groupid为该用户包含的groupid后23位，devtype和devid为对应设备分组包含的设备'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'][1:23],self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,400)
    def test_device_groups_delete_groupid_22(self):
        '''登录普通用户，传入groupid为该用户包含的groupid中间22位，devtype和devid为对应设备分组包含的设备'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'][1:22],self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,400)
    def test_device_groups_delete_groupid_null(self):
        '''登录普通用户，传入groupid为该用户包含的groupid中间22位，devtype和devid为对应设备分组包含的设备'''
        self.result = delete_device_test(self.base_url,self.user_0,'',self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,404)
    def test_device_groups_delete_groupid_of_other_user(self):
        '''登录普通用户，传入groupid为其他用户包含的groupid，devtype和devid为对应设备分组包含的设备'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_1_device_group_0['groupid'],self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,404)
    def test_device_groups_delete_device_of_other_group(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，devtype和devid为非该设备分组所包含的设备'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'],self.user_0_device_group_1['devices'][0]['devtype'],self.user_0_device_group_1['devices'][0]['devid'],1)
        self.assertEqual(self.result,400)
    def test_device_groups_delete_devtype_wrong(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，devtype和devid不对应'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'],'temprature',self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,400)
    def test_device_groups_delete_devtype_ls_1(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，devtype少一位字符'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'],self.user_0_device_group_0['devices'][0]['devtype'][:-1],self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,400)
    def test_device_groups_delete_devtype_null(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，devtype为空'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'],'',self.user_0_device_group_0['devices'][0]['devid'],1)
        self.assertEqual(self.result,400)
    def test_device_groups_delete_devid_wrong(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，devtype和devid不对应'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'],self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'][:-1],1)
        self.assertEqual(self.result,404)
    # def test_device_groups_delete_devid_null(self): ###存在Bug
    #     '''登录普通用户，传入groupid为该用户包含的groupid，devtype和devid不对应'''
    #     self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'],'','',1)
    #     self.assertEqual(self.result,405)
    # def test_device_groups_delete_devid_devtype_null(self): ##用例未确认有效
    #     '''登录普通用户，传入groupid为该用户包含的groupid，devtype和devid不对应'''
    #     self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'],self.user_0_device_group_0['devices'][0]['devtype'],'',1)
    #     self.assertEqual(self.result,405)
    def test_device_groups_delete_not_login(self):
        '''不登录，传入groupid为该用户包含的groupid，devtype和devid不对应'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'],self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],0)
        self.assertEqual(self.result,401)
    def test_device_groups_delete_logout(self):
        '''登录后退出，传入groupid为该用户包含的groupid，devtype和devid不对应'''
        self.result = delete_device_test(self.base_url,self.user_0,self.user_0_device_group_0['groupid'],self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],2)
        self.assertEqual(self.result,401)

if __name__ == '__main__':
    for n in range(53,55):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()



