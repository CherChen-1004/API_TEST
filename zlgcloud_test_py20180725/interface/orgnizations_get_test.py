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

def get_orgnizations_test(url,login_user,filter="",skip="",limit="",aggregation="",login_or_not=1):
    '''参数化编程，agent_or_user：登录代理商/普通用户=1/0，user_agent：传入的代理商/普通用户，login_or_not:是否登录，默认登录'''
    if (filter == ''and skip == '' and limit == '' and aggregation == '') == True:
        base_url = url
    else:
        base_url = url + '?' + filter + skip + limit + aggregation
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
        if aggregation == "":
            r.json()['data'].sort(key=str)
            return r.json()['data']
        else:
            return r.json()['count']
    else:
        return r.status_code

class OrgnizationsGetTest(unittest.TestCase):   ###创建orgnizationname为含有中文的组织时，查询结果为400   其他测试用例均已覆盖
    '''查询满足条件的组织，
    每条测试用例前提条件：创建两个代理商，每个代理商创建两个组织，创建两个普通用户'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/orgnizations"
        self.TestData = InitialData(41,43,43,44)
        self.user_arr = self.TestData.create_users()
        self.agent_arr = self.TestData.several_orgnizations_for_each_agent(2)
        # print(self.agent_arr)
    def tearDown(self):
        print(self.result)
        # self.TestData.delete_all_agents_and_orgnizations()
        self.TestData.delete_all_users()
    def test_get_orgnizations_agent_null(self):
        '''登录代理商用户，传入参数为空'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'])
    def test_get_orgnizations_agent_orgnizationname_1(self):
        '''登录代理商用户，传入orgnizationname=该代理商用户包含的其中一个'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[0]['orgnization_arr'][1]['orgnizationname'] +'%22%7D','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][1:])
    def test_get_orgnizations_agent_orgnizationname_other(self):
        '''登录代理商用户，传入orgnizationname=存在的但非该代理商包含的'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[1]['orgnization_arr'][1]['orgnizationname'] +'%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_orgnizationname_not_exist(self):
        '''登录代理商用户，传入orgnizationname=不存在的符合规则orgnizationname'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+ 'abcdefgh' +'%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_orgnizationname_ls_1(self):
        '''登录代理商用户，传入orgnizationname=少一位字符的orgnizationname'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][1]['orgnizationname'][:-1] +'%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_orgnizationid_1(self):
        '''登录代理商用户，传入orgnizationid=该代理商包含的一个'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationid%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][1]['orgnizationid'] +'%22%7D','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][1:])
    def test_get_orgnizations_agent_orgnizationid_other(self):
        '''登录代理商用户，传入orgnizationid=存在的但非该代理商包含的'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationid%22%3A%20%22'+self.agent_arr[0]['username'] +'%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_orgnizationid_not_exsit(self):
        '''登录代理商用户，传入orgnizationid=不存在的符合规则orgnizationid'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationid%22%3A%20%22'+ 'a1b2c3d4e5f6d7s8s9f0abcd' +'%22%7D','','','',1)
        self.assertEqual(self.result,500)
    def test_get_orgnizations_agent_orgnizationid_ls_1(self):
        '''登录代理商用户，传入orgnizationid=少一位字符的orgnizationid'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationid%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][1]['orgnizationid'][:-1] +'%22%7D','','','',1)
        self.assertEqual(self.result,500)
    def test_get_orgnizations_agent_owner_self(self):
        '''登录代理商用户，传入owner=本身'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22owner%22%3A%20%22'+ self.agent_arr[0]['username'] + '%22%7D','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'])
    def test_get_orgnizations_agent_owner_other(self):       #####存在Bug
        '''登录代理商用户，传入owner=其他用户名'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22owner%22%3A%20%22'+ self.agent_arr[1]['username'] + '%22%7D','','','',1)
        self.assertEqual(self.result,400)
    def test_get_orgnizations_agent_owner_not_exist(self):         ##存在Bug
        '''登录代理商用户，传入owner=不存在的用户名'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22owner%22%3A%20%22'+ 'abcdefgh' + '%22%7D','','','',1)
        self.assertEqual(self.result,400)
    def test_get_orgnizations_agent_owner_ls_1(self):             ##存在Bug
        '''登录代理商用户，传入owner=本身username少一位'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22owner%22%3A%20%22'+ self.agent_arr[0]['username'][:-1] + '%22%7D','','','',1)
        self.assertEqual(self.result,400)
    def test_get_orgnizations_agent_desc_self_1(self):
        '''登录代理商用户，传入desc = 本身包含的一个'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22desc%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][0]['desc'] + '%22%7D','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][:-1])
    def test_get_orgnizations_agent_desc_other(self):
        '''登录代理商用户，传入desc = 非本身包含的一个'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22desc%22%3A%20%22'+ self.agent_arr[1]['orgnization_arr'][0]['desc'] + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_desc_not_exist(self):
        '''登录代理商用户，传入desc = 不存在的desc'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22desc%22%3A%20%22'+ 'abcdefghigj' + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_desc_self_ls_1(self):
        '''登录代理商用户，传入desc = 本身包含的一个少一位字符'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22desc%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][0]['desc'][:-1] + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_address_self_1(self):
        '''登录代理商用户，传入address = 本身包含的一个'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22address%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][0]['address'] + '%22%7D','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][:-1])
    def test_get_orgnizations_agent_address_other(self):
        '''登录代理商用户，传入address = 非本身包含的一个'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22address%22%3A%20%22'+ self.agent_arr[1]['orgnization_arr'][0]['address'] + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_address_not_exist(self):
        '''登录代理商用户，传入address = 不存在的address'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22address%22%3A%20%22'+ 'abcdefghigj' + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_address_self_ls_1(self):
        '''登录代理商用户，传入address = 本身包含的一个少一位字符'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22address%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][0]['address'][:-1] + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_skip_0(self):
        '''登录代理商用户，传入skip=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=0','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'])
    def test_get_orgnizations_agent_skip_1(self):
        '''登录代理商用户，传入skip=1'''
        self.result = len(get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=1','','',1))
        self.assertEqual(self.result,1)
    def test_get_orgnizations_agent_skip_2(self):
        '''登录代理商用户，传入skip=2'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=2','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_skip_3(self):
        '''登录代理商用户，传入skip=3'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=3','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_limit_0(self):
        '''登录代理商用户，传入limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','','limit=0','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'])
    def test_get_orgnizations_agent_limit_1(self):
        '''登录代理商用户，传入limit=1'''
        self.result = len(get_orgnizations_test(self.base_url,self.agent_arr[0],'','','limit=1','',1))
        self.assertEqual(self.result,1)
    def test_get_orgnizations_agent_limit_2(self):
        '''登录代理商用户，传入limit=2'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','','limit=2','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'])
    def test_get_orgnizations_agent_limit_3(self):
        '''登录代理商用户，传入limit=2'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','','limit=3','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'])
    def test_get_orgnizations_agent_aggregation(self):
        '''登录代理商用户，传入aggregation=count'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','','','aggregation=count',1)
        self.assertEqual(self.result,2)
    def test_get_orgnizations_agent_orgnizationname_skip_0(self):
        '''登录代理商用户，传入orgnizationname=其中包含的一个和skip=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[0]['orgnization_arr'][0]['orgnizationname'] +'%22%7D','&skip=0','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][:-1])
    def test_get_orgnizations_agent_orgnizationname_skip_1(self):
        '''登录代理商用户，传入orgnizationname=其中包含的一个和skip=1'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[0]['orgnization_arr'][0]['orgnizationname'] +'%22%7D','&skip=1','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_orgnizationname_not_exist_skip_0(self):
        '''登录代理商用户，传入orgnizationname=不存在的orgnizationname和skip=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[1]['orgnization_arr'][0]['orgnizationname'] +'%22%7D','&skip=1','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_orgnizationname__limit_0(self):
        '''登录代理商用户，传入orgnizationname=本身包含的orgnization和limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[0]['orgnization_arr'][0]['orgnizationname'] +'%22%7D','','&limit=0','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][:-1])
    def test_get_orgnizations_agent_orgnizationname__limit_1(self):
        '''登录代理商用户，传入orgnizationname=本身包含的orgnization和limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[0]['orgnization_arr'][0]['orgnizationname'] +'%22%7D','','&limit=1','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][:-1])
    def test_get_orgnizations_agent_orgnizationname_not_exist__limit_1(self):
        '''登录代理商用户，传入orgnizationname=不存在的orgnizationname和limit=1'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[1]['orgnization_arr'][0]['orgnizationname'] +'%22%7D','','&limit=1','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_skip_0_limit_0(self):
        '''登录代理商用户，传入skip=0和limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=0','&limit=0','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'])
    def test_get_orgnizations_agent_skip_0_limit_1(self):
        '''登录代理商用户，传入skip=0和limit=1'''
        self.result = len(get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=0','&limit=1','',1))
        self.assertEqual(self.result,1)
    def test_get_orgnizations_agent_skip_0_limit_2(self):
        '''登录代理商用户，传入skip=0和limit=2'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=0','&limit=2','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'])
    def test_get_orgnizations_agent_skip_1_limit_0(self):
        '''登录代理商用户，传入skip=0和limit=0'''
        self.result = len(get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=1','&limit=0','',1))
        self.assertEqual(self.result,1)
    def test_get_orgnizations_agent_skip_1_limit_1(self):
        '''登录代理商用户，传入skip=0和limit=0'''
        self.result = len(get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=1','&limit=1','',1))
        self.assertEqual(self.result,1)
    def test_get_orgnizations_agent_skip_1_limit_2(self):
        '''登录代理商用户，传入skip=0和limit=0'''
        self.result = len(get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=1','&limit=2','',1))
        self.assertEqual(self.result,1)
    def test_get_orgnizations_agent_skip_2_limit_0(self):
        '''登录代理商用户，传入skip=0和limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=2','&limit=1','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_skip_2_limit_1(self):
        '''登录代理商用户，传入skip=0和limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=2','&limit=1','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_skip_2_limit_2(self):
        '''登录代理商用户，传入skip=0和limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','skip=2','&limit=2','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_orgnizationname_skip_1_limit_1_aggregation_count(self):
        '''登录代理商用户，传入orgnizationname=本身包含的orgnization和limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[0]['orgnization_arr'][0]['orgnizationname'] +'%22%7D','&skip=1','&limit=1','&aggregation=count',1)
        self.assertEqual(self.result,1)
    def test_get_orgnizations_agent_skip_0_limit_2_aggregation_count(self):
        '''登录代理商用户，skip=0 limit=2  aggregation=count'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'','&skip=0','&limit=2','&aggregation=count',1)
        self.assertEqual(self.result,2)
    def test_get_orgnizations_agent_orgnizationname_skip_0_limit_0(self):
        '''登录代理商用户，传入orgnizationname=本身包含的orgnization和limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[0]['orgnization_arr'][0]['orgnizationname'] +'%22%7D','&skip=0','&limit=0','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][:-1])
    def test_get_orgnizations_agent_orgnizationname_skip_1_limit_0(self):
        '''登录代理商用户，传入orgnizationname=本身包含的orgnization和limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.agent_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[0]['orgnization_arr'][0]['orgnizationname'] +'%22%7D','&skip=1','&limit=0','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_agent_orgnizationname_logout(self):
        '''登录后退出'''
        self.result = get_orgnizations_test(self.base_url, self.agent_arr[0],"",'', '', '', 2)
        self.assertEqual(self.result, 401)
    def test_get_orgnizations_agent_orgnizationname_not_login(self):
        '''不登陆'''
        self.result = get_orgnizations_test(self.base_url, self.agent_arr[0],"",'', '', '', 0)
        self.assertEqual(self.result, 401)
    def test_get_orgnizations_user_null(self):
        '''登录普通用户，传入参数为空'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],"",'','','',1)
        orgnization_arr = []
        for agent in self.agent_arr:
            for orgnization in agent['orgnization_arr']:
                orgnization_arr.append(orgnization)
        orgnization_arr.sort(key=str)
        self.assertEqual(self.result,orgnization_arr)
    def test_get_orgnizations_user_orgnizationname_1(self):
        '''登录普通用户，传入orgnizationname=该代理商用户包含的其中一个'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+self.agent_arr[0]['orgnization_arr'][1]['orgnizationname'] +'%22%7D','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][1:])
    def test_get_orgnizations_user_orgnizationname_not_exist(self):
        '''登录普通用户，传入orgnizationname=不存在的符合规则orgnizationname'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+ 'abcdefgh' +'%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_user_orgnizationname_ls_1(self):
        '''登录普通用户，传入orgnizationname=少一位字符的orgnizationname'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22orgnizationname%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][1]['orgnizationname'][:-1] +'%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_user_orgnizationid_1(self):
        '''登录普通用户，传入orgnizationid=该代理商包含的一个'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22orgnizationid%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][1]['orgnizationid'] +'%22%7D','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][1:])
    def test_get_orgnizations_user_orgnizationid_not_exsit(self):
        '''登录普通用户，传入orgnizationid=不存在的符合规则orgnizationid'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22orgnizationid%22%3A%20%22'+ 'a1b2c3d4e5f6d7s8s9f0abcd' +'%22%7D','','','',1)
        self.assertEqual(self.result,500)
    def test_get_orgnizations_user_orgnizationid_ls_1(self):
        '''登录普通用户，传入orgnizationid=少一位字符的orgnizationid'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22orgnizationid%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][1]['orgnizationid'][:-1] +'%22%7D','','','',1)
        self.assertEqual(self.result,500)
    def test_get_orgnizations_user_owner_self(self):
        '''登录普通用户，传入owner=本身'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22owner%22%3A%20%22'+ self.agent_arr[0]['username'] + '%22%7D','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'])
    def test_get_orgnizations_user_owner_not_exist(self):
        '''登录普通用户，传入owner=不存在的用户名'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22owner%22%3A%20%22'+ 'abcdefgh' + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_user_owner_ls_1(self):
        '''登录普通用户，传入owner=本身username少一位'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22owner%22%3A%20%22'+ self.agent_arr[0]['username'][:-1] + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_user_desc_self_1(self):
        '''登录普通用户，传入desc = 本身包含的一个'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22desc%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][0]['desc'] + '%22%7D','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][:-1])
    def test_get_orgnizations_user_desc_not_exist(self):
        '''登录普通用户，传入desc = 不存在的desc'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22desc%22%3A%20%22'+ 'abcdefghigj' + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_user_desc_self_ls_1(self):
        '''登录普通用户，传入desc = 本身包含的一个少一位字符'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22desc%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][0]['desc'][:-1] + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_user_address_self_1(self):
        '''登录普通用户，传入address = 本身包含的一个'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22address%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][0]['address'] + '%22%7D','','','',1)
        self.assertEqual(self.result,self.agent_arr[0]['orgnization_arr'][:-1])
    def test_get_orgnizations_user_address_not_exist(self):
        '''登录普通用户，传入address = 不存在的address'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22address%22%3A%20%22'+ 'abcdefghigj' + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_user_address_self_ls_1(self):
        '''登录普通用户，传入address = 本身包含的一个少一位字符'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'filter=%7B%22address%22%3A%20%22'+ self.agent_arr[0]['orgnization_arr'][0]['address'][:-1] + '%22%7D','','','',1)
        self.assertEqual(self.result,[])
    def test_get_orgnizations_user_skip_0(self):
        '''登录普通用户，传入skip=0'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'','skip=0','','',1)
        orgnization_arr = []
        for agent in self.agent_arr:
            for orgnization in agent['orgnization_arr']:
                orgnization_arr.append(orgnization)
        orgnization_arr.sort(key=str)
        self.assertEqual(self.result,orgnization_arr)
    def test_get_orgnizations_user_skip_1(self):
        '''登录普通用户，传入skip=1'''
        self.result = len(get_orgnizations_test(self.base_url,self.user_arr[0],'','skip=1','','',1))
        self.assertEqual(self.result,3)
    def test_get_orgnizations_user_skip_2(self):
        '''登录普通用户，传入skip=2'''
        self.result = len(get_orgnizations_test(self.base_url,self.user_arr[0],'','skip=2','','',1))
        self.assertEqual(self.result,2)
    def test_get_orgnizations_user_skip_3(self):
        '''登录普通用户，传入skip=3'''
        self.result = len(get_orgnizations_test(self.base_url,self.user_arr[0],'','skip=3','','',1))
        self.assertEqual(self.result,1)
    def test_get_orgnizations_user_limit_0(self):
        '''登录普通用户，传入limit=0'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'','','limit=0','',1)
        orgnization_arr = []
        for agent in self.agent_arr:
            for orgnization in agent['orgnization_arr']:
                orgnization_arr.append(orgnization)
        orgnization_arr.sort(key=str)
        self.assertEqual(self.result,orgnization_arr)
    def test_get_orgnizations_user_limit_1(self):
        '''登录普通用户，传入limit=1'''
        self.result = len(get_orgnizations_test(self.base_url,self.user_arr[0],'','','limit=1','',1))
        self.assertEqual(self.result,1)
    def test_get_orgnizations_user_limit_2(self):
        '''登录普通用户，传入limit=2'''
        self.result = len(get_orgnizations_test(self.base_url,self.user_arr[0],'','','limit=2','',1))
        self.assertEqual(self.result,2)
    def test_get_orgnizations_user_limit_3(self):
        '''登录普通用户，传入limit=2'''
        self.result = len(get_orgnizations_test(self.base_url,self.user_arr[0],'','','limit=3','',1))
        self.assertEqual(self.result,3)
    def test_get_orgnizations_user_aggregation(self):
        '''登录普通用户，传入aggregation=count'''
        self.result = get_orgnizations_test(self.base_url,self.user_arr[0],'','','','aggregation=count',1)
        self.assertEqual(self.result,4)
if __name__ == '__main__':
    unittest.main()
