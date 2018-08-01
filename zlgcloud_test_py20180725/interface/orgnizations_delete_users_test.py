#coding=utf_8
#Author = Cher Chan
import unittest
import requests
'''返回码如下：
            200	操作成功
            401	没有登录
            404   不存在
            500	服务器错误'''
from db_fixture.test_data import UsersForTest   #用于导入测试数据
from db_fixture.test_data import InitialData
def orgnization_delete_users_test(url,login_user,orgnizationid,username,login_or_not=1):
    '''参数化测试用例'''
    base_url = url + orgnizationid +'/members/' + username
    session = requests.Session()
    agent = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        agent.login()
        r = session.delete(base_url)
    elif login_or_not == 2:
        agent.login()
        agent.logout()
        r = session.delete(base_url)
    else:
        r = requests.delete(base_url)
    # print(r.json())
    return r.status_code

class OrgnizationDeleteUsersTest(unittest.TestCase):    ###已覆盖完整
    '''从组织移出用户接口测试'''
    def setUp(self):
        self.base_url = 'https://zlab.zlgcloud.com/v1/orgnizations/'
        self.TestData = InitialData(31, 33, 33, 37)
        self.agents_orgnizations_users_arr = self.TestData.create_agents_orgnizations_staff(2,1)
        self.agent_0_orgnization_0 = self.agents_orgnizations_users_arr[0]['orgnization_arr'][0]
        self.agent_0_orgnization_1 = self.agents_orgnizations_users_arr[0]['orgnization_arr'][1]
        self.agent_1_orgnization_0 = self.agents_orgnizations_users_arr[1]['orgnization_arr'][0]
        self.agent_0_orgnization_0_user_0 = self.agent_0_orgnization_0['members'][0]
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_users()
    def test_orgnization_delete_users_right(self):
        '''登录代理商用户，传入该代理商用户的一个组织ID，和已经包含的一个用户的username'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_0_orgnization_0['orgnizationid'],self.agent_0_orgnization_0['members'][0]['username'])
        print('username:',self.agent_0_orgnization_0['members'][0]['username'])
        self.assertEqual(self.result,200)
    def test_orgnization_delete_orgnizationid_23_1(self):
        '''登录代理商用户，传入该代理商用户的一个组织ID的前23位，和已经包含的一个用户的usernamec'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_0_orgnization_0['orgnizationid'][:-1],self.agent_0_orgnization_0_user_0['username'])
        self.assertEqual(self.result,400)
    def test_orgnization_delete_orgnizationid_23_2(self):
        '''登录代理商用户，传入该代理商用户的一个组织ID的前23位，和已经包含的一个用户的usernamec'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_0_orgnization_0['orgnizationid'][0:23],self.agent_0_orgnization_0_user_0['username'])
        self.assertEqual(self.result,400)
    def test_orgnization_delete_orgnizationid_22(self):
        '''登录代理商用户，传入该代理商用户的一个组织ID的中间22位，和已经包含的一个用户的username'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_0_orgnization_0['orgnizationid'][1:23],self.agent_0_orgnization_0_user_0['username'])
        self.assertEqual(self.result,400)
    def test_orgnization_delete_orgnizationid_of_other_agent(self):
        '''登录代理商用户，传入其他代理商的组织ID，和已经包含的一个用户的username'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_1_orgnization_0['orgnizationid'],self.agent_0_orgnization_0_user_0['username'])
        self.assertEqual(self.result,404)
    def test_orgnization_delete_orgnizationid_not_exist(self):
        '''登录代理商用户，传入一个不存在的ID，和已经包含的一个用户的username'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],'**********0123456789abcd',self.agent_0_orgnization_0_user_0['username'])
        self.assertEqual(self.result,500)
    def test_orgnization_delete_username_null(self):
        '''登录代理商用户，传入一个该代理商的组织ID，和一个空的username'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_0_orgnization_0['orgnizationid'],'',1)
        self.assertEqual(self.result,405)
    def test_orgnization_delete_username_not_exist(self):
        '''登录代理商用户，传入一个该代理商的组织ID，和一个不存在的username'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_0_orgnization_0['orgnizationid'],'sadtwer',1)
        self.assertEqual(self.result,400)
    def test_orgnization_delete_username_of_other_orgnization(self):
        '''登录代理商用户，传入一个该代理商的组织ID，和一个不存在的username'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_0_orgnization_0['orgnizationid'],self.agent_0_orgnization_1['members'][0]['username'],1)
        self.assertEqual(self.result,404)
    def test_orgnization_delete_username_of_other_agent(self):
        '''登录代理商用户，传入一个该代理商的组织ID，和一个不存在的username'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_0_orgnization_0['orgnizationid'],self.agent_1_orgnization_0['members'][0]['username'],1)
        self.assertEqual(self.result,404)
    def test_orgnization_delete_not_login(self):
        '''不登录，传入一个存在的ID，和一个该组织包含的username'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_0_orgnization_0['orgnizationid'],self.agent_0_orgnization_0_user_0['username'],0)
        self.assertEqual(self.result,401)
    def test_orgnization_delete_logout(self):
        '''登录后退出，传入一个存在的ID，和一个该组织包含的username'''
        self.result = orgnization_delete_users_test(self.base_url,self.agents_orgnizations_users_arr[0],self.agent_0_orgnization_0['orgnizationid'],self.agent_0_orgnization_0_user_0['username'],2)
        self.assertEqual(self.result,401)

if __name__ == '__main__':
    unittest.main()
