#coding=utf_8
#Author = Cher Chan
import unittest
import requests
from db_fixture.test_data import InitialData
'''返回码如下：
            200	操作成功
            401	没有登录
            404 不存在
            500	服务器错误'''
from db_fixture.test_data import UsersForTest   #用于导入测试数据
from db_fixture.test_data import InitialData

def delete_orgnization_test(url,login_user,orgnizationid,login_or_not=1):
    '''构建删除组织函数'''
    base_url = url + orgnizationid
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.delete(base_url)
    elif login_or_not == 0:
        r = session.delete(base_url)
    else:
        user.login()
        user.logout()
        r = session.delete(base_url)
    if r.status_code == 200:
        orgnization_arr = user.get_orgnizations().json()['data']
        orgnization_arr.sort(key=str)
        return orgnization_arr
    else:
        return r.status_code
class OrgnizationDeleteTest(unittest.TestCase):
    '''删除指定组织接口测试
    每条用例前提条件：创建两个代理商，每个代理商创建两个组织，创建两个普通用户'''
    def setUp(self):
        self.base_url = 'https://zlab.zlgcloud.com/v1/orgnizations/'
        self.TestData = InitialData(28,30,30,31)
        self.agents_orgnizations_arr = self.TestData.several_orgnizations_for_each_agent(2)
        self.ordinary_users = self.TestData.create_users()
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_users()
    def test_delete_orgnization_right(self):
        '''登录代理商用户，创建一个组织，获取该组织的organizationid，传入该组织的organizationid'''
        self.result = delete_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],1)
        self.assertEqual(self.result,self.agents_orgnizations_arr[0]['orgnization_arr'][1:])
    def test_delete_orgnization_23_1(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该组织的前23字符的orgnizationid'''
        self.result = delete_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'][:-1],1)
        self.assertEqual(self.result,400)
    def test_delete_orgnization_23_2(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该组织的后23字符的orgnizationid'''
        self.result = delete_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'][1:],1)
        self.assertEqual(self.result,400)
    def test_delete_orgnization_25(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入该组织的25字符的orgnizationid'''
        self.result = delete_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid']+'a',1)
        self.assertEqual(self.result,400)
    def test_delete_orgnization_orgnization_of_other_agent(self):
        '''登录代理商用户，创建一个组织，获取该组织的orgnizationid，传入其他代理商的orgnizationid'''
        self.result = delete_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[1]['orgnization_arr'][0]['orgnizationid'],1)
        self.assertEqual(self.result,404)
    def test_delete_orgnization_not_login(self):
        '''不登录，直接传入存在的组织ID'''
        self.result = delete_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],0)
        self.assertEqual(self.result,401)
    def test_delete_orgnization_logout(self):
        '''登录后退出，直接传入存在的组织ID'''
        self.result = delete_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],2)
        self.assertEqual(self.result,401)
    def test_delete_orgnization_ordinary_user_login(self):
        '''登录普通用户，直接传入存在的组织ID'''
        self.result = delete_orgnization_test(self.base_url,self.ordinary_users[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],1)
        self.assertEqual(self.result,403)
    def test_delete_orgnization_delete_and_check(self):
        '''登录代理商用户，删除代理商，登录普通用户，查询代理商所对应的组织是否全被删除'''
        session = requests.Session()
        agent = UsersForTest(int(self.agents_orgnizations_arr[0]['mobile'][-2:]),session)
        agent.login()
        agent.delete_users()
        user = UsersForTest(int(self.ordinary_users[0]['mobile'][-2:]),session)
        user.login()
        self.result = user.get_orgnizations(filter='filter=%7B%22owner%22%3A%20%22'+self.agents_orgnizations_arr[0]['username'] +'%22%7D').json()['data']
        self.assertEqual(self.result,[])
if __name__ == '__main__':
    for n in range(28,32):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()
