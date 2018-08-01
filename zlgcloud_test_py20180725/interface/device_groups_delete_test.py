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
def delete_device_groups_test(url,login_user,groupid,login_or_not=1):
    '''参数化编程，agent_or_user：登录代理商/普通用户=1/0，user_agent：传入的代理商/普通用户，login_or_not:是否登录，默认登录'''
    base_url = url + groupid
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
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

class DeviceGroupsDeleteTest(unittest.TestCase):
    '''删除设备分组接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/device_groups/"
        self.TestData = InitialData(55, 55, 55, 57)
        self.users_device_groups = self.TestData.create_users_device_groups(2)
        self.user_0 = self.users_device_groups[0]
        self.user_1 = self.users_device_groups[1]
    def tearDown(self):
        print(self.result)
        # self.TestData.delete_all_agents_and_orgnizations()
        self.TestData.delete_all_users()
    def test_delete_device_group_right(self):
        '''登录普通用户，传入该用户包含的设备分组的groupid'''
        self.result = delete_device_groups_test(self.base_url,self.user_0,self.user_0['device_groups'][0]['groupid'],1)
        self.assertEqual(self.result, 200)
    def test_delete_device_group_groupid_ls_1(self):
        '''登录普通用户，传入该用户包含的设备分组的groupid少一位字符'''
        self.result = delete_device_groups_test(self.base_url,self.user_0,self.user_0['device_groups'][0]['groupid'][:-1],1)
        self.assertEqual(self.result, 400)
    def test_delete_device_group_groupid_wrong(self):
        '''登录普通用户，传入错误的groupid'''
        self.result = delete_device_groups_test(self.base_url,self.user_0,'0a1b2d3d4s5s6g7s8d9s0s1s2f3g',1)
        self.assertEqual(self.result, 400)
    def test_delete_device_group_groupid_of_other_user(self):
        '''登录普通用户，传入其他用户用户包含的设备分组的groupid'''
        self.result = delete_device_groups_test(self.base_url,self.user_0,self.user_1['device_groups'][0]['groupid'],1)
        self.assertEqual(self.result, 404)
    def test_delete_device_group_not_login(self):
        '''不登陆'''
        self.result = delete_device_groups_test(self.base_url,self.user_0,self.user_0['device_groups'][0]['groupid'],0)
        self.assertEqual(self.result, 401)
    def test_delete_device_group_logout(self):
        '''登录后退出'''
        self.result = delete_device_groups_test(self.base_url,self.user_0,self.user_0['device_groups'][0]['groupid'],2)
        self.assertEqual(self.result, 401)
if __name__ == '__main__':
    unittest.main()