#coding=utf_8
#Author=Cher Chan

#已调试，可用
import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
'''返回码如下：
            200	操作成功
            401	没有登录
            403	没有权限
            500	服务器错误'''

def create_device_groups_test(base_url,login_user,payload ={},login_or_not=1):
    session = requests.Session()
    num = int(login_user['mobile'][-2:])
    user = UsersForTest(num,session)
    if login_or_not == 1:
        user.login()
        r = session.post(base_url,json=payload)
    elif login_or_not == 0:
        r = requests.post(base_url,json=payload)
    else:
        user.login()
        user.logout()
        r = session.post(base_url,json=payload)
    if r.status_code == 201:
        groupid = r.json()['data']['groupid']
        user.login()
        user.delete_device_groups(groupid)
    return r.status_code

class DeviceGroupsCreateTest(unittest.TestCase):
    '''创建新设备分组接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com/v1/device_groups"
        self.TestData = InitialData(50,51,51,53)
        self.user_arr = self.TestData.create_users()
        self.agent_arr = self.TestData.create_agents()
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_users()
    def test_create_device_groups_right_num(self):
        '''登录普通用户，传入符合规则的groupname和desc,传入字符全为数字'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"123456789","desc":"5464654"},1)
        self.assertEqual(self.result,201)
    def test_create_device_groups_right_letter(self):
        '''登录普通用户，传入符合规则的groupname和desc,传入字符全为字母'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"ksjdghhsidf","desc":"kjsdfhg"},1)
        self.assertEqual(self.result,201)
    def test_create_device_groups_right_mark(self):
        '''登录普通用户，传入符合规则的groupname和desc,传入字符全为特殊字符'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"____*******","desc":"***)))))))"},1)
        self.assertEqual(self.result,201)
    def test_create_device_groups_right(self):
        '''登录普通用户，传入符合规则的groupname和desc,传入字符为数字、字母、符号组合'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"IJHGI_122","desc":"hii___4545)"},1)
        self.assertEqual(self.result,201)
    def test_create_device_groups_groupname_char_num(self):
        '''登录普通用户，传入符合规则的groupname和desc,传入字符为数字、字母、符号组合'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"IJHGI_122"},1)
        self.assertEqual(self.result,201)
    def test_create_device_groups_groupname_only(self):
        '''登录普通用户，只传入符合规则的groupname'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"IJHGI_122"},1)
        self.assertEqual(self.result,201)
#     ###添加中文字符创建
    def test_create_device_groups_desc_only(self):
        '''登录普通用户，只传入符合规则的desc'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"desc":"hii___4545)"},1)
        self.assertEqual(self.result,400)
    def test_create_device_groups_groupname_1(self):
        '''登录普通用户，传入1位字符的groupname和符合规则的desc'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"desc":"hii___4545)"},1)
        self.assertEqual(self.result,400)
    def test_create_device_groups_groupname_2(self):
        '''登录普通用户，传入2位字符的groupname和符合规则的desc'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"ab","desc":"hii___4545)"},1)
        self.assertEqual(self.result,201)
    def test_create_device_groups_groupname_64(self):
        '''登录普通用户，传入32位字符的groupname和符合规则的desc'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"*"*64,"desc":"hii___4545)"},1)
        self.assertEqual(self.result,201)
    def test_create_device_groups_groupname_65(self):
        '''登录普通用户，传入33位字符的groupname和符合规则的desc'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"*"*65,"desc":"hii___4545)"},1)
        self.assertEqual(self.result,400)
    def test_create_device_groups_desc_0(self):
        '''登录普通用户，传入符合规则的groupname和0位字符的desc'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"asdfgsdrg","desc":""},1)
        self.assertEqual(self.result,201)
    def test_create_device_groups_desc_1024(self):
        '''登录普通用户，传入符合规则的groupname和1024位字符的desc'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"asdfgsdrg","desc":"*"*1024},1)
        self.assertEqual(self.result,201)
    def test_create_device_groups_desc_1025(self):
        '''登录普通用户，传入符合规则的groupname和1025位字符的desc'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"asdfgsdrg","desc":"*"*1025},1)
        self.assertEqual(self.result,400)
    #添加中文
    def test_create_device_groups_groupname_exist(self):        ##存在Bug
        '''登录普通用户，创建一个设备分组，再创建一个同名的设备分组'''
        result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"123456789","desc":"5464654"},1)
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"123456789","desc":"5464654"},1)
        self.assertEqual(self.result,201)
# ###不同用户创建同名分组
#     ##不同用户创建同名分组，再查询信息
    def test_create_device_groups_agent_login(self):
        '''登录代理商，传入符合规则的groupname和desc,传入字符全为数字'''
        self.result = create_device_groups_test(self.base_url,self.agent_arr[0],{"groupname":"123456789","desc":"5464654"},1)
        self.assertEqual(self.result,403)
    def test_create_device_groups_not_login(self):
        '''不登录'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"123456789","desc":"5464654"},0)
        self.assertEqual(self.result,401)
    def test_create_device_groups_logout(self):
        '''登录后再退出'''
        self.result = create_device_groups_test(self.base_url,self.user_arr[0],{"groupname":"123456789","desc":"5464654"},2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    unittest.main()











