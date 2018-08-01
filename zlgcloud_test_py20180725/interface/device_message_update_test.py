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
            404 设备不存在
            500	服务器错误'''

def update_device_message_test(url, login_user, devtype, devid,payload,login_or_not=1):
    '''参数化编程，login_user:登录的用户信息，login_or_not:是否登录，1：登录，0：不登录，2：登录后退出'''
    base_url = url + devid + '?devtype=' + devtype
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]), session)
    if login_or_not == 1:
        user.login()
        r = session.put(base_url,json=payload)
    elif login_or_not == 0:
        r = session.put(base_url, json=payload)
    else:
        user.login()
        user.logout()
        r = session.put(base_url, json=payload)
    if r.status_code == 200:
        print(r.json())
        result = r.json()['data']
        return result
    else:
        return r.status_code


class DevicesMessageUpdateTest(unittest.TestCase):  #####与开发确认数据的取值范围  &对自由设备的信息更新。。
    '''更新设备信息接口查询 接口测试'''

    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/devices/"
        self.TestData = InitialData(79, 79, 79,81)
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
    def test_update_device_message_right(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid'''
        payload = {"desc":"sdgfassdgf斯蒂芬&&&wgsat98"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)['desc']
        self.assertEqual(self.result,"sdgfassdgf斯蒂芬&&&wgsat98")
    def test_update_device_message_devtype_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和少一位字符的devtype'''
        payload = {"desc":"sdgfassdgf斯蒂芬&&&wgsat98"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'][:-1],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_devtype_wrong(self):
        '''登录普通用户，传入该用户所包含设备的devid和错误的devtype'''
        payload = {"desc":"sdgfassdgf斯蒂芬&&&wgsat98"}
        self.result = update_device_message_test(self.base_url,self.user_0,'stgerwe',self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_devid_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devtype和少一位字符devid'''
        payload = {"desc":"sdgfassdgf斯蒂芬&&&wgsat98"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'][:-1],payload,1)
        self.assertEqual(self.result,404)
    def test_update_device_message_devid_not_exist(self):
        '''登录普通用户，传入该用户所包含设备的devtype和不存在的devid'''
        payload = {"desc":"sdgfassdgf斯蒂芬&&&wgsat98"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],'sdrgerhdgfbwe45',payload,1)
        self.assertEqual(self.result,404)
    def test_update_device_message_devid_no_owner(self):
        '''登录普通用户，传入无owner的设备的devtype和devid'''
        payload = {"desc":"sdgfassdgf斯蒂芬&&&wgsat98"}
        self.result = update_device_message_test(self.base_url,self.user_0,'inverter','api_test_inverter_55',payload,1)['desc']
        self.assertEqual(self.result,"sdgfassdgf斯蒂芬&&&wgsat98")
    def test_update_device_message_other_user(self):
        '''登录普通用户，传入其他用户所包含设备的devtype和devid'''
        payload = {"desc":"sdgfassdgf斯蒂芬&&&wgsat98"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,403)
    def test_update_device_message_desc_0(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid，desc为0位字符'''
        payload = {"desc":""}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)['desc']
        self.assertEqual(self.result,"")
    def test_update_device_message_desc_1024(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid，desc为1024位字符'''
        payload = {"desc":"a"*256}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)['desc']
        self.assertEqual(self.result,"a"*256)
    def test_update_device_message_desc_256_chinese(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid，desc为256位中文字符'''
        payload = {"desc":"我"*256}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)['desc']
        self.assertEqual(self.result,"我"*256)
    def test_update_device_message_desc_257(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid，desc为257位字符'''
        payload = {"desc":"a"*257}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_devid(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入devid的更新信息'''
        payload = {"devid":"dfgdfg"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_devid_and_desc(self):    ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info中传入devid和desc的更新值'''
        payload = {"devid":"dfgdfg","desc":"sgwegwegvsdgesr7896"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_model(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入model的更新信息'''
        payload = {"model":"AB000"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_model_and_desc(self):    ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入model和desc的更新信息'''
        payload = {"model":"AB000","desc":"seogfhsogdh9we4t"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_registertime(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入registertime的更新信息'''
        payload = {"registertime":456457587}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_registertime_and_desc(self):    ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入registertime和desc的更新信息'''
        payload = {"registertime":45758656,"desc":"seogfhsogdh9we4t"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_onlinetime(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入onlinetime的更新信息'''
        payload = {"onlinetime":456457587}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_onlinetime_and_desc(self):    ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入onlinetime和desc的更新信息'''
        payload = {"onlinetime":45758656,"desc":"seogfhsogdh9we4t"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_devtype(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入devtype的更新信息'''
        payload = {"devtype":'rtgergh'}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_devtype_and_desc(self):    ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入devtype和desc的更新信息'''
        payload = {"devtype":'sdgfdsg',"desc":"seogfhsogdh9we4t"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_owner(self):
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入owner的更新信息'''
        payload = {"devtype":'rtgergh'}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_owner_and_desc(self):    ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devtype和devid，info传入devtype和desc的更新信息'''
        payload = {"owner":'sdgfdsg',"desc":"seogfhsogdh9we4t"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_message_not_login(self):
        '''不登录，传入该用户所包含设备的devtype和devid'''
        payload = {"desc":"sdgfassdgf斯蒂芬&&&wgsat98"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,0)
        self.assertEqual(self.result,401)
    def test_update_device_message_logout(self):
        '''不登录，传入存在的设备的devtype和devid'''
        payload = {"desc":"sdgfassdgf斯蒂芬&&&wgsat98"}
        self.result = update_device_message_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],payload,2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    for n in range(79,81):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()

