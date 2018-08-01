#coding=utf_8
#Author = Cher Chan
import unittest
import requests
'''返回码如下：
            200	操作成功
            401	没有登录
            404 不存在
            500	服务器错误'''

from db_fixture.test_data import UsersForTest   #用于导入测试数据
from db_fixture.test_data import InitialData

def add_users_test(url,login_user,orgnizationid,payload,login_or_not=1):
    base_url = url + orgnizationid + "/members"
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.post(base_url,json=payload)
    elif login_or_not == 2:
        user.login()
        user.logout()
        r = session.post(base_url,json=payload)
    else:
        r = requests.post(base_url,json=payload)
    return r.status_code

class OrgnizationAddUsersTest(unittest.TestCase):
    '''添加用户到组织接口测试
    每条测试用例前提条件：创建两个代理商，每个代理商创建两个组织，创建两个员工用户'''
    def setUp(self):
        self.base_url = 'https://zlab.zlgcloud.com/v1/orgnizations/'
        self.TestData = InitialData(25, 27, 27,28)
        self.agents_orgnizations_arr = self.TestData.several_orgnizations_for_each_agent(2)
        self.agent_0_orgnization_0 = self.agents_orgnizations_arr[0]['orgnization_arr'][0]
        self.staff_arr = self.TestData.create_staff()
    def tearDown(self):
        print(self.result)
        # self.TestData.delete_all_agents_and_orgnizations()
        self.TestData.delete_all_users()
    def test_orgnization_add_users_test_right_role_0(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该id、一个已存在的username和role=0'''
        payload = {"username":self.staff_arr[0]['username'],"role":0}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,1)
        self.assertEqual(self.result,200)
    def test_orgnization_add_users_test_right_role_1(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该id、一个已存在的username	和role=1'''
        payload = {"username":self.staff_arr[0]['username'],"role":1}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,1)
        self.assertEqual(self.result,200)
    def test_orgnization_add_users_test_right_role_2(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该id、一个已存在的username	和role=2'''
        payload = {"username":self.staff_arr[0]['username'],"role":3}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,1)
        self.assertEqual(self.result,200)
    def test_orgnization_add_users_test_right_role_3(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该id、一个已存在的username	和role=3'''
        payload = {"username":self.staff_arr[0]['username'],"role":3}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,1)
        self.assertEqual(self.result,200)
    def test_orgnization_add_users_test_right_role_4(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该id、一个已存在的username	和role=4'''
        payload = {"username":self.staff_arr[0]['username'],"role":4}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,1)
        self.assertEqual(self.result,400)
    def test_orgnization_add_users_test_orgnizationid_23_1(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该id的前23位、一个已存在的username	和role=0'''
        payload = {"username":self.staff_arr[0]['username'],"role":0}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'][:-1],payload,1)
        self.assertEqual(self.result,400)
    def test_orgnization_add_users_test_orgnizationid_22(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该id的中间22位、一个已存在的username	和role=0'''
        payload = {"username":self.staff_arr[0]['username'],"role":0}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'][1:22],payload,1)
        self.assertEqual(self.result,400)
    def test_orgnization_add_users_test_orgnizationid_23_2(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该id的后23位、一个已存在的username	和role=0'''
        payload = {"username":self.staff_arr[0]['username'],"role":0}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'][1:],payload,1)
        self.assertEqual(self.result,400)
    def test_orgnization_add_users_test_username_null(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该ID、空的username和role=0'''
        payload = {"role":0}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,1)
        self.assertEqual(self.result,400)
    def test_orgnization_add_users_test_username_wrong(self): ###存在Bug
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该ID、不存在的username和role=0'''
        payload = {"username":'dfgert34tdfv',"role":0}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,1)
        self.assertEqual(self.result,400)
    def test_orgnization_add_users_test_username_1(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该ID、一个字符的username和role=0'''
        payload = {"username":'g',"role":0}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,1)
        self.assertEqual(self.result,400)

    def test_orgnization_add_users_test_user_included(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，只传入一个已经包含的username'''
        payload = {"username":self.staff_arr[0]['username'],"role":0}
        r = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,1)
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,1)
        self.assertEqual(self.result,400)
    def test_orgnization_add_users_test_logout(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，退出登录，再传入一个已存在的username和role=0'''
        payload = {"username":self.staff_arr[0]['username'],"role":0}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,0)
        self.assertEqual(self.result,401)
    def test_orgnization_add_users_test_not_login(self):
        '''不登陆，再传入一个已存在的ID,username和role=0'''
        payload = {"username":self.staff_arr[0]['username'],"role":0}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agent_0_orgnization_0['orgnizationid'],payload,2)
        self.assertEqual(self.result,401)
    def test_orgnization_add_users_test_orgnizationid_of_other(self):  ##存在Bug
        '''传入一个其他代理商的组织ID'''
        payload = {"username":self.staff_arr[0]['username'],"role":0}
        self.result = add_users_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[1]['orgnization_arr'][1]['orgnizationid'],payload,1)
        self.assertEqual(self.result,400)

if __name__ == '__main__':
    for n in range(25,29):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()
