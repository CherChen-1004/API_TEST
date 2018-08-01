#coding=utf_8
#Author = CherChan
import unittest
import requests
'''返回码如下：
            201	操作成功
            401	没有登录
            403	没有权限
            500	服务器错误'''
from db_fixture.test_data import UsersForTest   #用于导入测试数据
from db_fixture.test_data import InitialData
def create_orgnization_test(base_url,login_user,payload,login_or_not=1):
    '''创建组织函数，用例参数化'''
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.post(base_url,json=payload)
    elif login_or_not == 0:
        r = requests.post(base_url,json=payload)
    else:
        user.login()
        user.logout()
        r = session.post(base_url,json=payload)
    print(r.json())
    return r.status_code

class OrgnizationCreateTest(unittest.TestCase):
    '''创建组织接口测试
    每个用例前提条件：两个代理商，创建两个普通用户'''
    def setUp(self):
        self.base_url = 'https://zlab.zlgcloud.com/v1/orgnizations'
        self.TestData = InitialData(22,24,24,25)
        self.agents_arr = self.TestData.create_agents()
        self.users_arr = self.TestData.create_users()
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_users()
    def test_create_orgnization_right(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的organizationname、desc、address'''
        payload = {"orgnizationname": 'abc***123----',"desc": 'abc___123***@@@',"address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload,login_or_not=1)
        self.assertEqual(self.result, 201)
    def test_create_orgnization_orgnizationname_null(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的desc、address和空的organizationname'''
        payload = {"orgnizationname": '',"desc": 'abc___123***@@@',"address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload,login_or_not=1)
        self.assertEqual(self.result, 400)
    def test_create_orgnization_orgnizationname_1(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的desc、address和1位字符的organizationname'''
        payload = {"orgnizationname":'a', "desc": 'abc___123***@@@', "address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload,login_or_not=1)
        self.assertEqual(self.result, 400)
    def test_create_orgnization_orgnizationname_2(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的desc、address和2位字符的organizationname'''
        payload = {"orgnizationname": 'ab', "desc": 'abc___123***@@@', "address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload,login_or_not=1)
        self.assertEqual(self.result, 201)
    def test_create_orgnization_orgnizationname_64(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的desc、address和32位字符的organizationname'''
        payload = {"orgnizationname": 'aaaaaaaaa1111111111__________aaaaaaaaaa1111111111__________@@@@', "desc": 'abc___123***@@@', "address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 201)
    def test_create_orgnization_orgnizationname_65(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的desc、address和33位字符的organizationname'''
        payload = {"orgnizationname": 'aaaaaaaaaa1111111111__________aaaaaaaaaa1111111111__________@@@@#', "desc": 'abc___123***@@@', "address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 400)
    def test_create_orgnization_orgnizationname_chinese_1(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的desc、address和1位中文字符的organizationname'''
        payload = {"orgnizationname": '美', "desc": 'abc___123***@@@', "address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 400)
    def test_create_orgnization_orgnizationname_chinese_2(self):
        payload = {"orgnizationname": '美丽', "desc": 'abc___123***@@@', "address": 'abc___123***@@@'}
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的desc、address和2位中文字符的organizationname'''
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 201)
    def test_create_orgnization_orgnizationname_chinese_64(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的desc、address和2位中文字符的organizationname'''
        payload = {"orgnizationname": '美'*64, "desc": 'abc___123***@@@', "address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 201)
    def test_create_orgnization_orgnizationname_chinese_65(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的desc、address和2位中文字符的organizationname'''
        payload = {"orgnizationname": '美'*65, "desc": 'abc___123***@@@', "address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 400)
    def test_create_orgnization_desc_null(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的username、address和空的desc'''
        payload = {"orgnizationname": '美丽', "desc": '', "address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 201)
    def test_create_orgnization_desc_1024(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的username、address和1024个字符的desc'''
        payload = {"orgnizationname": '美丽', "desc": 'd'*1024, "address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 201)
    def test_create_orgnization_desc_1025(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的username、address和1025个字符的desc'''
        payload = {"orgnizationname": '美丽', "desc": 'd'*1025, "address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 400)
    def test_create_orgnization_address_null(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的organizationname、desc和空的address	'''
        payload = {"orgnizationname": '美丽', "desc": 'fyjhdftyd', "address": ''}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 201)
    def test_create_orgnization_address_256(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的organizationname、desc和空的256个字符的address'''
        payload = {"orgnizationname": '美丽', "desc": 'gfsd', "address": 'a'*256}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 201)
    def test_create_orgnization_address_257(self):
        '''创建一个代理商用户，然后用该用户登录，传入符合要求的organizationname、desc和空的257个字符的address'''
        payload = {"orgnizationname": '美丽', "desc": 'd'*1025, "address": 'd'*257}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload)
        self.assertEqual(self.result, 400)
    def test_create_orgnization_not_login(self):
        '''创建一个代理商用户，不登陆，传入符合要求的organizationname、desc和address'''
        payload = {"orgnizationname": 'abc***123----',"desc": 'abc___123***@@@',"address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload,login_or_not=0)
        self.assertEqual(self.result, 401)
    def test_create_orgnization_logout(self):
        '''创建一个代理商用户，不登陆，传入符合要求的organizationname、desc和address'''
        payload = {"orgnizationname": 'abc***123----',"desc": 'abc___123***@@@',"address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload,login_or_not=2)
        self.assertEqual(self.result, 401)
    def test_create_orgnization_orgnization_exist(self):
        '''创建一个代理商用户，然后用该用户登录，传入其他代理商已创建的组织的orgnizationname'''
        payload = {"orgnizationname": 'abc***123----',"desc": 'abc___123***@@@',"address": 'abc___123***@@@'}
        result = create_orgnization_test(self.base_url,self.agents_arr[0],payload,login_or_not=1)
        self.result = create_orgnization_test(self.base_url,self.agents_arr[1],payload,login_or_not=1)
        self.assertEqual(self.result, 500)
    def test_create_orgnization_orgnization_exist_2(self):
        '''创建一个代理商用户，然后用该用户登录，传入该代理商已创建的组织的orgnizationname'''
        payload = {"orgnizationname": 'abc***123----',"desc": 'abc___123***@@@',"address": 'abc___123***@@@'}
        result = create_orgnization_test(self.base_url,self.agents_arr[0],payload,login_or_not=1)
        self.result = create_orgnization_test(self.base_url,self.agents_arr[0],payload,login_or_not=1)
        self.assertEqual(self.result, 500)

    def test_create_orgnization_not_agent(self):
        '''创建一个普通用户，然后用户登录，传入符合要求的organizationname、desc和address'''
        payload = {"orgnizationname": 'abc***123----',"desc": 'abc___123***@@@',"address": 'abc___123***@@@'}
        self.result = create_orgnization_test(self.base_url,self.users_arr[0],payload,login_or_not=1)
        self.assertEqual(self.result, 403)

if __name__ == '__main__':
    unittest.main()
