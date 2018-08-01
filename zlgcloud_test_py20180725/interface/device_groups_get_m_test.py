# coding=utf_8
# Author=Cher Chan
import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
'''返回码如下：
            200	操作成功
            401	没有登录
            404	设备分组不存在
            500	服务器错误'''
def get_device_groups_message_test(base_url, login_user, groupid, login_or_not=1):
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]), session)
    if login_or_not == 1:
        user.login()
        r = session.get(base_url + groupid)
    elif login_or_not == 0:
        r = requests.get(base_url + groupid)
    else:
        user.login()
        user.logout()
        r = session.get(base_url + groupid)
    if r.status_code == 200:
        result = r.json()
        del result['jwt']
        return result
    else:
        return r.status_code

class DeviceGroupsGetMessageTest(unittest.TestCase):
    '''获取设备分组信息接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/device_groups/"
        self.TestData = InitialData(58, 58, 58, 60)
        self.users_s_device_groups = self.TestData.create_users_device_groups(2)
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_users()
    def test_get_device_groups_user_right(self):
        '''登录普通用户，传入该用户包含的groupid，判断返回的status_code和data'''
        self.result = get_device_groups_message_test(self.base_url,self.users_s_device_groups[0],self.users_s_device_groups[0]['device_groups'][0]['groupid'],1)
        self.assertEqual(self.result,self.users_s_device_groups[0]['device_groups'][0])
    def test_get_device_groups_user_groupid_23_1(self):
        '''登录普通用户，传入该用户包含的groupid前23位，判断返回的status_code'''
        self.result = get_device_groups_message_test(self.base_url,self.users_s_device_groups[0],self.users_s_device_groups[0]['device_groups'][0]['groupid'][:-1],1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_groupid_23_2(self):
        '''登录普通用户，传入该用户包含的groupid后23位，判断返回的status_code'''
        self.result = get_device_groups_message_test(self.base_url,self.users_s_device_groups[0],self.users_s_device_groups[0]['device_groups'][0]['groupid'][1:23],1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_groupid_of_other_user(self):
        '''登录普通用户，传入其他用户包含的groupid，判断返回的status_code'''
        self.result = get_device_groups_message_test(self.base_url,self.users_s_device_groups[0],self.users_s_device_groups[1]['device_groups'][0]['groupid'],1)
        self.assertEqual(self.result,404)
    def test_get_device_groups_user_groupid_not_exist(self):
        '''登录普通用户，传入不存在的groupid，判断返回的status_code'''
        self.result = get_device_groups_message_test(self.base_url,self.users_s_device_groups[0],'abcdefghij01234567890123',1)
        self.assertEqual(self.result,500)
    def test_get_device_groups_user_not_login(self):
        '''不登录，传入该用户包含的groupid，判断返回的status_code和data'''
        self.result = get_device_groups_message_test(self.base_url,self.users_s_device_groups[0],self.users_s_device_groups[0]['device_groups'][0]['groupid'],0)
        self.assertEqual(self.result,401)
    def test_get_device_groups_user_logout(self):
        '''登录后退出，传入该用户包含的groupid，判断返回的status_code和data'''
        self.result = get_device_groups_message_test(self.base_url,self.users_s_device_groups[0],self.users_s_device_groups[0]['device_groups'][0]['groupid'],2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    unittest.main()