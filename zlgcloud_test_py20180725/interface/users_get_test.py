#coding=utf_8
#Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
'''返回码如下：
            200	操作成功
            401	没有登录
            403	没有权限
            500	服务器错误'''
def get_users_test(url,login_user,filter="",skip="",limit="",aggregation="",login_or_not=1):
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
            users_arr = r.json()['data']
            for user_data in users_arr:
                del user_data['last_login_time']
                del user_data['password_changed_time']
                del user_data['last_login_ip']
                # del user_data['password_changed_time']
            users_arr.sort(key=str)
            return users_arr
        else:
            return r.json()['count']
    else:
        return r.status_code

class UsersGetTest(unittest.TestCase):        ####登录代理商查询时，均不能正确查询
    '''查询满足条件的用户'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com/v1/users"
        self.TestData = InitialData(16,16,16,18)
        self.users_arr = self.TestData.create_users()
    def tearDown(self):
        print(self.result)
        # self.TestData.delete_all_agents_and_orgnizations()
        self.TestData.delete_all_users()
    def test_get_users_user_null(self):
        '''登录普通用户，用该用户登录然后传入该接口的网址'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'','','','',1)
        print([self.users_arr[0]])
        self.assertEqual(self.result,[self.users_arr[0]])
    def test_get_users_user_username(self):
        '''登录一个普通用户，用该用户登录然后传入filter=该用户的名称'''
        self.result = get_users_test(self.base_url,self.users_arr[0], 'filter=%7B%22username%22%3A%22' + self.users_arr[0]['username'] + '%22%7D', '', '', '', login_or_not=1)
        self.assertEqual(self.result, [self.users_arr[0]])
    def test_get_users_user_username_ls_1(self):
        '''登录一个普通用户，用该用户登录然后传入filter=该用户的名称少一位'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'filter=%7B%22username%22%3A%22' + self.users_arr[0]['username'][:-1] + '%22%7D', '','', '',1)
        self.assertEqual(self.result, [])
    def test_get_users_user_username_other(self):
        '''登录一个普通用户，用该用户登录然后传入filter=其他用户名'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'filter=%7B%22username%22%3A%22' + self.users_arr[1]['username'] + '%22%7D', '','', '',1)
        self.assertEqual(self.result, [])
    def test_get_users_user_mobile(self):
        '''登录一个普通用户，用该用户登录然后传入filter=该用户的手机号'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'filter=%7B%22mobile%22%3A%22' + self.users_arr[0]['mobile'] + '%22%7D', '','', '', 1)
        self.assertEqual(self.result, [self.users_arr[0]])
    def test_get_users_user_mobile_ls_1(self):
        '''登录一个普通用户，用该用户登录然后传入filter=该用户的手机号少一位'''
        self.result = get_users_test(self.base_url,self.users_arr[0], 'filter=%7B%22mobile%22%3A%22' + self.users_arr[0]['mobile'][:-1] + '%22%7D', '','', '',1)
        self.assertEqual(self.result, [])
    def test_get_users_user_mobile_other(self):
        '''登录一个普通用户，用该用户登录然后传入filter=其他mobile'''
        self.result = get_users_test(self.base_url,self.users_arr[0], 'filter=%7B%22mobile%22%3A%22' + self.users_arr[1]['mobile'] + '%22%7D', '','', '',1)
        self.assertEqual(self.result, [])
    def test_get_users_user_email(self):
        '''登录一个普通用户，用该用户登录然后传入filter=该用户的email地址'''
        self.result = get_users_test(self.base_url,self.users_arr[0], 'filter=%7B%22email%22%3A%22' + self.users_arr[0]['email'] + '%22%7D','','', '',1)
        self.assertEqual(self.result, [self.users_arr[0]])
    def test_get_users_user_email_ls(self):
        '''登录一个普通用户，用该用户登录然后传入filter=该用户的email地址'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'filter=%7B%22email%22%3A%22' + self.users_arr[0]['email'][:-2] + '%22%7D', '', '', '', 1)
        self.assertEqual(self.result, [])
    def test_get_users_user_email_other(self):
        '''登录一个普通用户，用该用户登录然后传入filter=其他email'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'filter=%7B%22email%22%3A%22' + self.users_arr[1]['email'] + '%22%7D', '', '', '', 1)
        self.assertEqual(self.result, [])
    def test_get_users_user_skip_0(self):
        '''登录一个普通用户，用该用户登录然后传入skip=0'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'', 'skip=0', '', '', 1)
        self.assertEqual(self.result, [self.users_arr[0]])
    def test_get_users_user_skip_1(self):
        '''登录一个普通用户，用该用户登录然后传入skip=1'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'', 'skip=1', '', '', 1)
        self.assertEqual(self.result, [])
    def test_get_users_user_limit_1(self):
        '''登录一个普通用户，用该用户登录然后传入limit=1'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'', '', 'limit=1', '', 1)
        self.assertEqual(self.result, [self.users_arr[0]])
    def test_get_users_user_limit_0(self):
        '''登录一个普通用户，用该用户登录然后传入limit=0'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'', '', 'limit=0', '', 1)
        self.assertEqual(self.result, [self.users_arr[0]])
    def test_get_users_user_aggregation_count(self):
        '''登录一个普通用户，用该用户登录然后传入aggregation=count'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'', '', '', 'aggregation=count', 1)
        self.assertEqual(self.result, 1)
    def test_get_users_user_skip_0_limit_1(self):
        '''登录一个普通用户，用该用户登录然后传入limit=1，skip=0'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'', 'skip=0','&limit=1', '', 1)
        self.assertEqual(self.result, [self.users_arr[0]])
    def test_get_users_user_skip_1_limit_0(self):
        '''登录一个普通用户，用该用户登录然后传入limit=0，skip=1'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'', 'skip=1','&limit=0', '', 1)
        self.assertEqual(self.result, [])
    def test_get_users_user_skip_1_limit_1(self):
        '''登录一个普通用户，用该用户登录然后传入limit=1，skip=1'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'', 'skip=1','&limit=1', '', 1)
        self.assertEqual(self.result, [])
    def test_get_users_user_username_skip_0_limit_1(self):
        '''登录一个普通用户，用该用户登录然后传入filter为username=该用户，limit=1，skip=0'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'filter=%7B%22username%22%3A%22'+ self.users_arr[0]['username']+'%22%7D', '&skip=0','&limit=1', '', 1)
        self.assertEqual(self.result, [self.users_arr[0]])
    def test_get_users_user_username_skip_0_limit_1_aggregation(self):
        '''登录一个普通用户，用该用户登录然后传入filter为username=该用户，limit=1，skip=0,aggregation=count'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'filter=%7B%22username%22%3A%22'+ self.users_arr[0]['username']+'%22%7D', '&skip=1','&limit=1', '&aggregation=count', 1)
        self.assertEqual(self.result, 1)
    def test_get_users_user_not_login(self):
        '''登录一个普通用户，不登陆，传入该接口网址'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'', '','', '', 0)
        self.assertEqual(self.result, 401)
    def test_get_users_user_logout(self):
        '''登录一个普通用户，不登陆，传入该接口网址'''
        self.result = get_users_test(self.base_url,self.users_arr[0],'', '','', '', 2)
        self.assertEqual(self.result, 401)

if __name__ == '__main__':
    user = UsersForTest(16)
    user.login()
    user.delete_users()
    user2 = UsersForTest(17)
    user2.login()
    user2.delete_users()
    unittest.main()
