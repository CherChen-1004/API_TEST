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

def update_orgnization_test(url,login_user,orgnizationid,payload,login_or_not=1):
    '''参数化测试用例'''
    base_url = url + orgnizationid
    session = requests.Session()
    agent = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        agent.login()
        r = session.put(base_url,json=payload)
    elif login_or_not == 2:
        agent.login()
        agent.logout()
        r = session.put(base_url,json=payload)
    else:
        r = requests.post(base_url,json=payload)
    return r.status_code

class OrgnizationUpdateTest(unittest.TestCase):   ###全部覆盖完成
    '''更新组织接口测试
    每条测试用例前提条件：创建两个代理商，每个代理商创建两个组织，创建一个普通用户'''
    def setUp(self):
        self.base_url = 'https://zlab.zlgcloud.com:443/v1/orgnizations/'
        self.TestData = InitialData(44, 46, 46, 47)
        self.agents_orgnizations_arr = self.TestData.several_orgnizations_for_each_agent(2)
        self.ordinary_users = self.TestData.create_users()
    def tearDown(self):
        print(self.result)
        # self.TestData.delete_all_agents_and_orgnizations()
        self.TestData.delete_all_users()
    def test_update_orgnization_orgnizationname_right(self):
        '''登录代理商用户，传入该代理商用户的一个组织id、info符合规则的orgnizationname'''
        payload = {"orgnizationname":"abcdef****___"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_desc_right(self):
        '''登录代理商用户，传入该代理商用户的一个组织id、info符合规则的desc'''
        payload = {"desc":"abcdef****___"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_address_right(self):
        '''登录代理商用户，传入该代理商用户的一个组织id、info符合规则的address'''
        payload = {"address":"abcdef****___"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_info_orgnizationid(self):
        '''登录代理商用户，传入该代理商用户的一个组织id、info符合规则的orgnizationid'''
        payload = {"orgnizationid":"5a3b1563c098c00008d1ffd9"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,400)
    def test_update_orgnization_info_owner(self):  ####存在Bug  ##已解决
        '''登录代理商用户，传入该代理商用户的一个组织id、info符合规则的存在的owner'''
        payload = {"owner":self.agents_orgnizations_arr[1]['username']}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,400)
    def test_update_orgnization_info_discoverable_true(self):   ###存在Bug  已解决
        '''登录代理商用户，传入该代理商用户的一个组织id、info discoverable为true'''
        payload_1 = {"discoverable":False}
        payload_2 = {"discoverable":True}
        r1 = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload_1,login_or_not=1)
        self.result = update_orgnization_test(self.base_url, self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'], payload_2, login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_info_discoverable_false(self):
        '''登录代理商用户，传入该代理商用户的一个组织id、info discoverable为false'''
        payload = {"discoverable":False}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_info_desc_address_orgnization_right(self):
        '''登录代理商用户，传入该代理商用户的一个组织id、info 传入符合规则的desc、address、orgnizationname'''
        payload = {"desc":"ashodgh)(*","address":"sd ose454","orgnizationname":"_________"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_info_orgnizationid_23_1(self):
        '''登录代理商用户，传入该代理商用户的一个组织id的后23位、info 传入符合规则的desc、address、orgnizationname'''
        payload = {"desc":"ashodgh)(*","address":"sd ose454","orgnizationname":"_________"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'][:-1],payload,login_or_not=1)
        self.assertEqual(self.result,400)
    def test_update_orgnization_info_orgnizationid_23_2(self):
        '''登录代理商用户，传入该代理商用户的一个组织id的前23位、info 传入符合规则的desc、address、orgnizationname'''
        payload = {"desc":"ashodgh)(*","address":"sd ose454","orgnizationname":"_________"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'][0:23],payload,login_or_not=1)
        self.assertEqual(self.result,400)
    def test_update_orgnization_info_orgnizationid_22(self):
        '''登录代理商用户，传入该代理商用户的一个组织id的前23位、info 传入符合规则的desc、address、orgnizationname'''
        payload = {"desc":"ashodgh)(*","address":"sd ose454","orgnizationname":"_________"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'][1:23],payload,login_or_not=1)
        self.assertEqual(self.result,400)
    def test_update_orgnization_info_other_orgnizationid(self):
        '''登录代理商用户，传入一个其他用户的组织ID、info 传入符合规则的desc、address、orgnizationname'''
        payload = {"desc":"ashodgh)(*","address":"sd ose454","orgnizationname":"_________"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[1]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,404)
    def test_update_orgnization_info_orgnizationid_not_exist(self):
        '''登录代理商用户，传入一个不存在的符合规则组织ID、info 传入符合规则的desc、address、orgnizationname'''
        payload = {"desc":"ashodgh)(*","address":"sd ose454","orgnizationname":"_________"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],'**********00000000001234',payload,login_or_not=1)
        self.assertEqual(self.result,500)
    def test_update_orgnization_info_desc_0(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入0位字符的desc'''
        payload = {"desc":""}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_info_desc_1024(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入1024位字符的desc'''
        payload = {"desc":"a"*1024}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_info_desc_1025(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入1025位字符的desc'''
        payload = {"desc":"a"*1025}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,400)
    def test_update_orgnization_info_address_0(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入0位字符的address'''
        payload = {"address":""}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_info_address_256(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入256位字符的address'''
        payload = {"address":"a"*256}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_info_address_257(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入257位字符的address'''
        payload = {"address":"a"*257}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,400)
    def test_update_orgnization_info_orgnizationname_1(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入1位字符的orgnizationname'''
        payload = {"orgnizationname":"a"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,400)
    def test_update_orgnization_info_orgnizationname_2(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入2位字符的orgnizationname'''
        payload = {"orgnizationname":"ab"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_info_orgnizationname_64(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入1位字符的orgnizationname'''
        payload = {"orgnizationname":"0123456789012345678901234567890123456789012345678901234567890123"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,200)
    def test_update_orgnization_info_orgnizationname_65(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入1位字符的orgnizationname'''
        payload = {"orgnizationname":"012345678901234567890123456789012345678901234567890123456789012345"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,400)
    def test_update_orgnization_info_orgnizationname_of_other_agent(self):
        '''登录代理商用户，传入一个符合规则的组织ID、info 传入被其他组织命名的的orgnizationname'''
        payload = {"orgnizationname":self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationname']}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[1],self.agents_orgnizations_arr[1]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=1)
        self.assertEqual(self.result,400)
    def test_update_orgnization_info_not_login(self):
        '''不登录，直接传入一个符合规则存在的组织ID、info 传入符合规则的orgnizationname'''
        payload = {"orgnizationname":"adsfsb"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=0)
        self.assertEqual(self.result,401)
    def test_update_orgnization_info_logout(self):
        '''登录代理商用户，然后退出，传入一个符合规则的组织ID、info 传入符合规则的orgnizationname'''
        payload = {"orgnizationname":"adsfsb"}
        self.result = update_orgnization_test(self.base_url,self.agents_orgnizations_arr[0],self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],payload,login_or_not=2)
        self.assertEqual(self.result,401)
    def test_update_orgnization_info_user_login(self):
        '''登录普通用户，传入一个符合规则的组织ID、info 传入符合规则的orgnizationname'''
        session = requests.Session()
        user = UsersForTest(47,session)
        user.create_users()
        user.login()
        payload = {"orgnizationname": "adsfsb"}
        r = session.put(self.base_url+self.agents_orgnizations_arr[0]['orgnization_arr'][0]['orgnizationid'],json=payload)
        self.result = r.status_code
        self.assertEqual(self.result,403)
        user.login()
        user.delete_users()

if __name__ == '__main__':
    for n in range(44,47):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
        user.delete_users()
    unittest.main()
