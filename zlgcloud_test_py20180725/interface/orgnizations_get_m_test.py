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
def get_orgnization_message_test(url,login_user,orgnizationid,login_or_not=1):
    base_url = url + orgnizationid
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
        data = r.json()
        del data['jwt']
        return data
    else:
        return r.status_code

class OrgnizationGetMessageTest(unittest.TestCase):
    '''返回指定组织接口测试
    每条测试用例前提条件：创建两个代理商，每个代理商创建两个组织，创建两个普通用户'''
    def setUp(self):
        self.base_url = 'https://zlab.zlgcloud.com/v1/orgnizations/'
        self.TestData = InitialData(37,39,39,41)
        self.agents_orgnizations_arr = self.TestData.several_orgnizations_for_each_agent(2)
        self.users_arr = self.TestData.create_users()
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_users()

    def test_get_orgnization_message_right(self):
        '''登录代理商用户，创建一个组织，获取改组织的orgnizationid，传入该orgnizationid'''
        self.result = get_orgnization_message_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],1)
        self.assertEqual(self.result,self.agents_orgnizations_arr[0]['orgnization_arr'][0])
    def test_get_orgnization_message_23_1(self):
        '''登录代理商用户，创建一个组织，传入前23位字符的orgnizationid'''
        self.result = get_orgnization_message_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'][:-1],1)
        self.assertEqual(self.result,400)
    def test_get_orgnization_message_23_2(self):
        '''登录代理商用户，创建一个组织，传入后23位字符的orgnizationid'''
        self.result = get_orgnization_message_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'][1:],1)
        self.assertEqual(self.result,400)
    def test_get_orgnization_message_25(self):
        '''登录代理商用户，创建一个组织，传入25位字符的orgnizationid'''
        self.result = get_orgnization_message_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid']+'a',1)
        self.assertEqual(self.result,400)
    def test_get_orgnization_message_not_exist(self):
        '''登录代理商用户，传入一个不存在的orgnizationid'''
        self.result = get_orgnization_message_test(self.base_url,self.agents_orgnizations_arr[0],"0d1r2e3d4s5g6f7f8f90d1d",1)
        self.assertEqual(self.result,400)
    def test_get_orgnization_message_orgnizationid_other_agent(self):
        '''登录代理商用户，传入一个其他代理商的orgnizationid'''
        self.result = get_orgnization_message_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[1]['orgnization_arr'][0]['orgnizationid'],1)
        self.assertEqual(self.result,404)
    def test_get_orgnization_message_logout(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，然后退出登录，传入该组织的orgnizationid'''
        self.result = get_orgnization_message_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],2)
        self.assertEqual(self.result,401)
    def test_get_orgnization_message_not_login(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，然后退出登录，传入该组织的orgnizationid'''
        self.result = get_orgnization_message_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],0)
        self.assertEqual(self.result,401)
    def test_get_orgnization_message_domestic_user(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，然后退出登录，用另一个普通用户登录，传入该组织的orgnizationid'''
        self.result = get_orgnization_message_test(self.base_url,self.users_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],1)
        self.assertEqual(self.result,403)
if __name__ == '__main__':
    unittest.main()
