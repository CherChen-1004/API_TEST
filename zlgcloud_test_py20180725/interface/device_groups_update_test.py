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
def update_device_groups_test(url,login_user,groupid,payload,login_or_not=1):
    '''参数化编程，login_user:登录的账号，login_or_not:是否登录，默认登录'''
    base_url = url + groupid
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.put(base_url,json=payload)
    elif login_or_not == 0:
        r = requests.put(base_url,json=payload)
    else:
        user.login()
        user.logout()
        r  = session.put(base_url,json=payload)
    return r.status_code

class DeviceGroupsUpdateTest(unittest.TestCase):
    '''更新设备分组信息接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/device_groups/"
        self.TestData = InitialData(64, 64, 64,66)
        self.users_device_groups_arr = self.TestData.create_users_device_groups(2)
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_users()

    def test_update_device_groups_right(self):
        '''登录普通用户，传入该用户包含的groupid，info填入符合规则的desc'''
        payload = {'desc':'abcddslfg'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,200)
    def test_update_device_groups_groupid_23(self):
        '''登录普通用户，传入该用户包含的groupid前23位字符，info填入符合规则的descsd'''
        payload = {'desc':'abcddslfg'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'][:-1],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_groups_groupid_23_2(self):
        '''登录普通用户，传入该用户包含的groupid后23位字符，info填入符合规则的desc'''
        payload = {'desc':'abcddslfg'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'][1:23],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_groups_groupid_22(self):
        '''登录普通用户，传入该用户包含的groupid中间22位字符，info填入符合规则的desc'''
        payload = {'desc':'abcddslfg'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'][1:22],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_groups_groupid_of_other_user(self):
        '''登录普通用户，传入其他用户包含的groupid，info填入符合规则的desc'''
        payload = {'desc':'abcddslfg'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[1]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,404)
    def test_update_device_groups_groupname_right(self):
        '''登录普通用户，传入该用户包含的groupid，info传入符合规则的groupname'''
        payload = {'groupname':'abcddslfg'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,200)
    def test_update_device_groups_groupname_1(self):
        '''登录普通用户，传入该用户包含的groupid，info传入一位字符的groupname'''
        payload = {'groupname':'a'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_groups_groupname_2(self):
        '''登录普通用户，传入该用户包含的groupid，info传入2位字符的groupname'''
        payload = {'groupname':'ab'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,200)
    def test_update_device_groups_groupname_64(self):
        '''登录普通用户，传入该用户包含的groupid，info传入32位字符的groupname'''
        payload = {'groupname': 'a'*64}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,200)
    def test_update_device_groups_groupname_65(self):
        '''登录普通用户，传入该用户包含的groupid，info传入33位字符的groupname'''
        payload = {'groupname': 'a'*65}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_groups_groupname_of_other_device_group(self):    ##存在BUG
        '''登录普通用户，传入该用户包含的groupid，info传入同用户包含的其他设备分组的groupname'''
        payload = {'groupname': self.users_device_groups_arr[0]['device_groups'][1]['groupname']}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,400)
    # def test_update_device_groups_groupname_of_other_user(self):  该用例存在争议
    #     '''登录普通用户，传入该用户包含的groupid，info传入同用户包含的其他设备分组的groupname'''
    #     payload = {'groupname': self.users_device_groups_arr[1]['device_groups'][0]['groupname']}
    #     self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
    #     self.assertEqual(self.result,400)
    def test_update_device_groups_info_groupid(self):
        '''登录普通用户，传入该用户包含的groupid，info传入groupid为24位字符'''
        payload = {'groupid': 'a1s2d3d4d5f6e7c8f9d00123'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_groups_info_owner(self):
        '''登录普通用户，传入该用户包含的groupid，info传入owner为符合规则的字符串'''
        payload = {'owner': self.users_device_groups_arr[1]['username']}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_groups_desc_0(self):
        '''登录普通用户，传入该用户包含的groupid，info传入desc为0位字符的字符串'''
        payload = {'desc': ''}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,200)
    def test_update_device_groups_desc_1024(self):
        '''登录普通用户，传入该用户包含的groupid，info传入desc为1024位字符的字符串'''
        payload = {'desc': 'a'*1024}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,200)
    def test_update_device_groups_desc_1025(self):
        '''登录普通用户，传入该用户包含的groupid，info传入desc为1025位字符的字符串'''
        payload = {'desc': 'a'*1025}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_groups_desc_groupname_right(self):
        '''登录普通用户，传入该用户包含的groupid，info传入groupname和desc为符合规则的字符串'''
        payload = {'desc': 'sdgsdfgh', 'groupname':'sg ewr g'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,1)
        self.assertEqual(self.result,200)
    def test_update_device_groups_not_login(self):
        '''不登录，直接传入存在的groupid和符合规则的desc'''
        payload = {'desc': 'sdgsdfgh'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,0)
        self.assertEqual(self.result,401)
    def test_update_device_groups_logout(self):
        '''登录后退出，直接传入存在的groupid和符合规则的desc'''
        payload = {'desc': 'sdgsdfgh'}
        self.result = update_device_groups_test(self.base_url,self.users_device_groups_arr[0],self.users_device_groups_arr[0]['device_groups'][0]['groupid'],payload,2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    unittest.main()





