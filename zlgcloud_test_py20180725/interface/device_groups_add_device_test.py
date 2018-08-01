#coding=utf_8
#Author=Cher Chan
import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
'''返回码如下：
            200	操作成功
            401	没有登录
            404 设备分组不存在
            500	服务器错误'''
def add_device_to_groups_test(url,login_user,groupid,payload,login_or_not=1):
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    base_url = url+groupid
    if login_or_not == 1:
        user.login()
        r = session.post(base_url,json=payload)
    elif login_or_not == 0:
        r = requests.post(base_url,json=payload)
    else:
        user.login()
        user.logout()
        r = session.post(base_url,json=payload)
    return r.status_code

class DeviceGroupsAddDeviceTest(unittest.TestCase):         ###测试该模块必须保证 "devid": "abcdef_1","devtype": "inverter"  的设备接入服务器，且不被其他用户添加
    '''添加设备到设备分组'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/device_groups/"
        self.TestData = InitialData(48,48,48,50)
        self.users_device_groups_arr = self.TestData.create_users_device_groups(2)
        # self.users_device_groups_arr = self.agents_orgnizations_users_device_groups[0]['orgnization_arr'][0]['members']
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_agents_and_orgnizations()
        self.TestData.delete_all_users()
    def test_delete_device_groups_right(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，info中传入存在的设备所对应的devid和devtype'''
        payload = {"devid": "api_test_inverter_0","devtype": "inverter"}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,200)
    def test_delete_device_groups_devid_only(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，info中只传入存在的设备所对应的devid'''
        payload = {"devid": "api_test_inverter_0"}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,400)
    def test_delete_device_groups_devtype_only(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，info中只传入存在的设备所对应的devtype'''
        payload = {"devtype": "inverter"}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,400)
    def test_delete_device_groups_groupid_23(self):
        '''登录普通用户，传入groupid为该用户包含的groupid的前23位'''
        payload = {"devid": "api_test_inverter_0", "devtype": "inverter"}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'][:-1],payload,1)
        self.assertEqual(self.result,400)
    def test_delete_device_groups_groupid_23_1(self):
        '''登录普通用户，传入groupid为该用户包含的groupid的前23位'''
        payload = {"devid": "api_test_inverter_0", "devtype": "inverter"}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'][1:23],payload,1)
        self.assertEqual(self.result,400)
    def test_delete_device_groups_groupid_22(self):
        '''登录普通用户，传入groupid为该用户包含的groupid的中间22位'''
        payload = {"devid": "api_test_inverter_0", "devtype": "inverter"}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'][1:22],payload,1)
        self.assertEqual(self.result,400)
    def test_delete_device_groups_groupid_of_other_user(self):
        '''登录普通用户，传入groupid为其他用户包含的groupid'''
        payload = {"devid": "api_test_inverter_0", "devtype": "inverter"}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[1]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,404)
    def test_delete_device_groups_not_exist(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，info中传入不存在的设备'''
        payload = {"devid": "sdarfhy t", "devtype": "inverter"}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[1]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,404)
    def test_delete_device_groups_devtype_null(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，info中传入不存在的设备'''
        payload = {"devid": "api_test_inverter_0", "devtype": ""}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[1]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,400)
    def test_delete_device_groups_devtype_wrong(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，info中传入的devtype与devid不对应'''
        payload = {"devid": "api_test_inverter_0", "devtype": "temperature"}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[1]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,404)
    def test_delete_device_groups_dev_of_other_user(self):
        '''登录普通用户，传入groupid为该用户包含的groupid，info传入已被其他用户添加的设备'''
        payload = {"devid": "api_test_inverter_0", "devtype": "inverter"}
        add_device_to_groups_test(self.base_url,self.users_device_groups_arr[1],self.users_device_groups_arr[1]['device_groups'][0]['groupid'],payload,1)
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[1]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,403)
    def test_delete_device_group_same_device_added_to_several_groups(self):
        '''一个设备添加到多个分组'''
        payload = {"devid": "abcdef_1","devtype": "inverter"}
        r1 = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][1]['groupid'],payload,1)
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,404)
    def test_delete_device_groups_added_to_same_group(self):##同一设备重复添加  提示已存在
        '''同一设备重复添加  提示已存在'''
        payload = {"devid": "api_test_inverter_0","devtype": "inverter"}
        result1 = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,400)
    def test_delete_device_groups_not_login(self):  ##用没被添加过的设备
        '''不登录，传入存在的groupid，info传入已被其他用户添加的设备'''
        payload = {"devid": "api_test_inverter_0", "devtype": "inverter"}
        add_device_to_groups_test(self.base_url,self.users_device_groups_arr[1],self.users_device_groups_arr[1]['device_groups'][0]['groupid'],payload,1)
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[1]['device_groups'][0]['groupid'],payload,0)
        self.assertEqual(self.result,401)
    def test_delete_device_groups_logout(self): ##用没被添加过的设备
        '''登录后再退出，传入存在的groupid，info传入已被其他用户添加的设备'''
        payload = {"devid": "api_test_inverter_0", "devtype": "inverter"}
        self.result = add_device_to_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[1]['device_groups'][0]['groupid'],payload,2)
        self.assertEqual(self.result,401)

    ##一个设备添加到多个分组
    ##同一设备重复添加  提示已存在
if __name__ == '__main__':
    for n in range(48,50):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()



