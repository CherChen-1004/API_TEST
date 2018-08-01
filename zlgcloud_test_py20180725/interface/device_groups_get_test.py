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
def get_device_groups_test(url,login_user,filter="",skip="",limit="",aggregation="",login_or_not=1):
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
            device_groups = r.json()['data']
            device_groups.sort(key=str)
            return device_groups
        else:
            return r.json()['count']
    else:
        return r.status_code

class DeviceGroupsGetMessageTest(unittest.TestCase):
    '''查询满足条件的设备分组接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/device_groups"
        self.TestData = InitialData(60, 60, 60, 62)
        self.users_device_groups = self.TestData.create_users_device_groups(2)
        self.user_0 = self.users_device_groups[0]
        self.user_1 = self.users_device_groups[1]
    def tearDown(self):
        print(self.result)
        # self.TestData.delete_all_agents_and_orgnizations()
        self.TestData.delete_all_users()
    def test_get_device_groups_user_null(self):
        '''登录普通用户，传入参数为空，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"","","","",1)
        self.assertEqual(self.result,self.user_0['device_groups'])
    def test_get_device_groups_user_filter_groupname_right(self):
        '''登录普通用户，传入filter为groupname=该用户包含的其中一个设备分组，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,self.user_0['device_groups'][:-1])
    def test_get_device_groups_user_filter_groupname_ls_1(self):
        '''登录普通用户，传入filter为groupname=该用户包含的其中一个设备分组groupname少一位字符，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'][:-1] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_filter_groupname_of_other_user(self):
        '''登录普通用户，传入filter为groupname=其他用户包含的其中一个设备分组groupname，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_1['device_groups'][0]['groupname'] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_filter_groupname_not_exist(self):
        '''登录普通用户，传入filter为groupname=不存在的设备分组groupname，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ 'abcdefghjk' + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_filter_groupid_right(self):
        '''登录普通用户，传入filter为groupid=该用户包含的其中一个设备分组groupid，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupid%22%3A%20%22"+ self.user_0['device_groups'][0]['groupid'] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,self.user_0['device_groups'][:-1])
    def test_get_device_groups_user_filter_groupid_23_1(self):
        '''登录普通用户，传入filter为groupid=该用户包含的其中一个设备分组groupid前23位，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupid%22%3A%20%22"+ self.user_0['device_groups'][0]['groupid'][:-1] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,500)
    def test_get_device_groups_user_filter_groupid_23_2(self):
        '''登录普通用户，传入filter为groupid=该用户包含的其中一个设备分组groupid后23位，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupid%22%3A%20%22"+ self.user_0['device_groups'][0]['groupid'][1:23] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,500)
    def test_get_device_groups_user_filter_groupid_22(self):#delete
        '''登录普通用户，传入filter为groupid=该用户包含的其中一个设备分组groupid中间22位，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupid%22%3A%20%22"+ self.user_0['device_groups'][0]['groupid'][1:22] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,500)
    def test_get_device_groups_user_filter_groupid_of_other_user(self):
        '''登录普通用户，传入filter为groupid=其他用户包含的其中一个设备分组groupid，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupid%22%3A%20%22"+ self.user_1['device_groups'][0]['groupid'] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_filter_groupid_not_exist(self):
        '''登录普通用户，传入filter为groupid=不存在的设备分组groupid，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupid%22%3A%20%22"+ 'a0b1c2d3e4g5r6w7f8d9f0g1' + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,500)

###desc 多个一致
    def test_get_device_groups_user_filter_desc_right(self):
        '''登录普通用户，传入filter为desc=该用户包含的其中一个设备分组desc，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22desc%22%3A%20%22"+ self.user_0['device_groups'][0]['desc'] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,self.user_0['device_groups'][:-1])
    def test_get_device_groups_user_filter_desc_ls_1(self):
        '''登录普通用户，传入filter为desc=该用户包含的其中一个设备分组desc少一位，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22desc%22%3A%20%22"+ self.user_0['device_groups'][0]['desc'][:-1] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_filter_desc_of_other_user(self):
        '''登录普通用户，传入filter为desc=其他用户包含的其中一个设备分组desc，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22desc%22%3A%20%22"+ self.user_1['device_groups'][0]['desc'] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_filter_desc_not_exist(self):
        '''登录普通用户，传入filter为desc=不存在的一个设备分组desc，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22desc%22%3A%20%22"+ 'sgderthreth' + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_filter_owner_right(self):
        '''登录普通用户，传入filter为owner=该用户包含的其中一个设备分组username，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22"+ self.user_0['username'] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,self.user_0['device_groups'])
    def test_get_device_groups_user_filter_owner_ls_1(self):
        '''登录普通用户，传入filter为owner=该用户包含的其中一个设备分组username少一位，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22"+ self.user_0['username'][:-1] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_filter_owner_of_other_user(self):
        '''登录普通用户，传入filter为owner=其他用户包含的其中一个设备分组username，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22"+ self.user_1['username'] + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_filter_owner_not_exist(self):
        '''登录普通用户，传入filter为owner=不存在的一个设备分组username，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22"+ 'sgderthreth' + "%22%7D" ,"","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_filter_created_time_right(self):  ###改成时间段
        '''登录普通用户，传入filter为created_time=该用户包含的其中一个设备分组created_time，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22created_time%22%3A"+ str(self.user_0['device_groups'][0]['created_time']) + "%7D","","","",1)
        if self.user_0['device_groups'][0]['created_time'] == self.user_0['device_groups'][1]['created_time']:
            result = self.user_0['device_groups']
        else:
            result = self.user_0['device_groups'][:-1]
        self.assertEqual(self.result,result)
    def test_get_device_groups_user_filter_created_time_ls_1(self):
        '''登录普通用户，传入filter为created_time=该用户包含的其中一个设备分组created_time少一位，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22created_time%22%3A"+ str(self.user_0['device_groups'][0]['created_time'])[:-1] + "%7D" ,"","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_filter_created_time_of_other_user(self):
        '''登录普通用户，传入filter为created_time=其他用户包含的其中一个设备分组created_time，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22created_time%22%3A"+ str(self.user_1['device_groups'][0]['created_time']) + "%7D","","","",1)
        if self.user_0['device_groups'][0]['created_time'] == self.user_0['device_groups'][1]['created_time']:
            result = self.user_0['device_groups']
        else:
            result = self.user_0['device_groups'][1:]
        self.assertEqual(self.result,result)
    def test_get_device_groups_user_filter_created_time_not_exist(self):
        '''登录普通用户，传入filter为created_time=不存在的一个设备分组created_time，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22created_time%22%3A%20"+ '1534888511' + "%7D" ,"","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_skip_0(self):
        '''登录普通用户，传入skip=0，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=0","","",1)
        self.assertEqual(self.result,self.user_0['device_groups'])
    def test_get_device_groups_user_skip_1(self):
        '''登录普通用户，传入skip=1，判断返回status_code和body内容'''
        self.result = len(get_device_groups_test(self.base_url,self.user_0,"" ,"skip=1","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_groups_user_skip_2(self):
        '''登录普通用户，传入skip=2，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=2","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_skip_3(self):
        '''登录普通用户，传入skip=3，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=3","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_skip_special_char(self):
        '''登录普通用户，传入skip=特殊字符，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=**&&((","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_skip_chinese_char(self):
        '''登录普通用户，传入skip=中文字符，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=中文字符","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_skip_english_char(self):
        '''登录普通用户，传入skip=英文字符，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=sdgfg","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_limit_0(self):
        '''登录普通用户，传入limit=0，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"","limit=0","",1)
        self.assertEqual(self.result,self.user_0['device_groups'])
    def test_get_device_groups_user_limit_1(self):
        '''登录普通用户，传入limit=1，判断返回status_code和body内容'''
        self.result = len(get_device_groups_test(self.base_url,self.user_0,"" ,"","limit=1","",1))
        self.assertEqual(self.result,1)
    def test_get_device_groups_user_limit_2(self):
        '''登录普通用户，传入limit=2，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"","limit=2","",1)
        self.assertEqual(self.result,self.user_0['device_groups'])
    def test_get_device_groups_user_limit_3(self):
        '''登录普通用户，传入limit=3，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"","limit=3","",1)
        self.assertEqual(self.result,self.user_0['device_groups'])
    def test_get_device_groups_user_limit_special_char(self):
        '''登录普通用户，传入limit=特殊字符，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"","limit=**&&((","",1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_limit_chinese_char(self):
        '''登录普通用户，传入limit=中文字符，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"","limit=中文字符","",1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_limit_english_char(self):
        '''登录普通用户，传入limit=英文字符，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"","limit=sdgfg","",1)
        self.assertEqual(self.result,400)
    def test_get_device_groups_user_aggregation_count(self):
        '''登录普通用户，传入aggregation=count，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"","","aggregation=count",1)
        self.assertEqual(self.result,2)
    def test_get_device_groups_user_groupname_skip_0(self):
        '''登录普通用户，传入filter=该用户包含的一个设备分组groupname和skip=0，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"&skip=0","","",1)
        self.assertEqual(self.result,self.user_0['device_groups'][:-1])
    def test_get_device_groups_user_groupname_skip_1(self):
        '''登录普通用户，传入filter=该用户包含的一个设备分组groupname和skip=1，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"&skip=1","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_groupname_skip_2(self):
        '''登录普通用户，传入filter=该用户包含的一个设备分组groupname和skip=2，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"&skip=2","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_groupname_limit_0(self):
        '''登录普通用户，传入filter=该用户包含的一个设备分组groupname和limit=0，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"","&limit=0","",1)
        self.assertEqual(self.result,self.user_0['device_groups'][:-1])
    def test_get_device_groups_user_groupname_limit_1(self):
        '''登录普通用户，传入filter=该用户包含的一个设备分组groupname和limit=1，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"","&limit=1","",1)
        self.assertEqual(self.result,self.user_0['device_groups'][:-1])
    def test_get_device_groups_user_groupname_limit_2(self):
        '''登录普通用户，传入filter=该用户包含的一个设备分组groupname和limit=2，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"","&limit=2","",1)
        self.assertEqual(self.result,self.user_0['device_groups'][:-1])
    def test_get_device_groups_user_groupname_agrregation_2(self):
        '''登录普通用户，传入filter=该用户包含的一个设备分组groupname和aggregation=count，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"","","&aggregation=count",1)
        self.assertEqual(self.result,1)
    def test_get_device_groups_user_skip_0_limit_0(self):
        '''登录普通用户，传入skip=0，limit=0，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=0","&limit=0","",1)
        self.assertEqual(self.result,self.user_0['device_groups'])
    def test_get_device_groups_user_skip_0_limit_1(self):
        '''登录普通用户，传入skip=0，limit=1，判断返回status_code和body内容'''
        self.result = len(get_device_groups_test(self.base_url,self.user_0,"" ,"skip=0","&limit=1","",1))
        self.assertEqual(self.result,1)
    def test_get_device_groups_user_skip_0_limit_2(self):
        '''登录普通用户，传入skip=0，limit=1，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=0","&limit=2","",1)
        self.assertEqual(self.result,self.user_0['device_groups'])
    def test_get_device_groups_user_skip_1_limit_0(self):
        '''登录普通用户，传入skip=1，limit=0，判断返回status_code和body内容'''
        self.result = len(get_device_groups_test(self.base_url,self.user_0,"" ,"skip=1","&limit=0","",1))
        self.assertEqual(self.result,1)
    def test_get_device_groups_user_skip_1_limit_1(self):
        '''登录普通用户，传入skip=1，limit=1，判断返回status_code和body内容'''
        self.result = len(get_device_groups_test(self.base_url,self.user_0,"" ,"skip=1","&limit=1","",1))
        self.assertEqual(self.result,1)
    def test_get_device_groups_user_skip_1_limit_2(self):
        '''登录普通用户，传入skip=1，limit=1，判断返回status_code和body内容'''
        self.result = len(get_device_groups_test(self.base_url,self.user_0,"" ,"skip=1","&limit=2","",1))
        self.assertEqual(self.result,1)
    def test_get_device_groups_user_skip_2_limit_0(self):
        '''登录普通用户，传入skip=2，limit=0，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=2","&limit=0","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_skip_2_limit_1(self):
        '''登录普通用户，传入skip=2，limit=1，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=2","&limit=1","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_skip_2_limit_2(self):
        '''登录普通用户，传入skip=2，limit=1，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"skip=2","&limit=2","",1)
        self.assertEqual(self.result,[])
    def test_get_device_groups_user_limit_1_aggregation_count(self):
        '''登录普通用户，传入limit=1，aggregation=count，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"" ,"","limit=1","&aggregation=count",1)
        self.assertEqual(self.result,2)
    def test_get_device_groups_user_groupname_skip_0_limit_0_aggregation_count(self):
        '''登录普通用户，传入filter=该用户包含的一个设备分组groupname，skip=0，limit=0，aggregation=count，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D"  ,"&skip=1","&limit=1","&aggregation=count",1)
        self.assertEqual(self.result,1)
    def test_get_device_groups_user_groupname_skip_1_limit_1_aggregation_count(self):
        '''登录普通用户，传入filter=该用户包含的一个设备分组groupname，skip=0，limit=0，aggregation=count，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D"  ,"&skip=1","&limit=1","&aggregation=count",1)
        self.assertEqual(self.result,1)
    def test_get_device_groups_user_groupname_skip_1_limit_0_aggregation_count(self):
        '''登录普通用户，传入filter=该用户包含的一个设备分组groupname，skip=0，limit=0，aggregation=count，判断返回status_code和body内容'''
        self.result = get_device_groups_test(self.base_url,self.user_0,"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D"  ,"&skip=1","&limit=0","&aggregation=count",1)
        self.assertEqual(self.result,1)
##不登录
##登录后退出

###  self.agent1_device_groups_arr   ###代理商查询权限待细分
    # def test_get_device_groups_agent_null(self):        ##有Bug
    #     '''登录代理商，传入参数为空，判断返回status_code和body内容'''
    #     self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"","","","",1)
    #     device_groups_arr = []
    #     for orgnization in self.agents_orgnizations_users_device_groups[0]['orgnization_arr']:
    #         for user in orgnization['members']:
    #             for device_group in user['device_groups']:
    #                 device_groups_arr.append(device_group)
    #     device_groups_arr.sort(key=str)
    #     self.assertEqual(self.result,device_groups_arr)
    # def test_get_device_groups_agent_filter_groupname_right(self):
    #     '''登录代理商，传入filter为groupname=该用户包含的其中一个设备分组，判断返回status_code和body内容'''
    #     self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"","","",1)
    #     self.assertEqual(self.result,self.user_0['device_groups'][:-1])
    # def test_get_device_groups_agent_filter_groupname_ls_1(self):
    #     '''登录代理商，传入filter为groupname=该用户包含的其中一个设备分组groupname少一位字符，判断返回status_code和body内容'''
    #     self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'][:-1] + "%22%7D" ,"","","",1)
    #     self.assertEqual(self.result,[])
    # def test_get_device_groups_agent_filter_groupname_of_other_user(self):
    #     '''登录代理商，传入filter为groupname=其他代理商包含的其中一个设备分组groupname，判断返回status_code和body内容'''
    #     self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.agents_orgnizations_users_device_groups[1]['device_groups'][0]['groupname'] + "%22%7D" ,"","","",1)
    #     self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_filter_groupname_not_exist(self):
#         '''登录代理商，传入filter为groupname=不存在的设备分组groupname，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ 'abcdefghjk' + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_filter_groupid_right(self):
#         '''登录代理商，传入filter为groupid=该用户包含的其中一个设备分组groupid，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupid%22%3A%20%22"+ self.user_0['device_groups'][0]['groupid'] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,self.user_0['device_groups'][:-1])
#     def test_get_device_groups_agent_filter_groupid_23_1(self):
#         '''登录代理商，传入filter为groupid=该用户包含的其中一个设备分组groupid前23位，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupid%22%3A%20%22"+ self.user_0['device_groups'][0]['groupid'][:-1] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,500)
#     def test_get_device_groups_agent_filter_groupid_23_2(self):
#         '''登录代理商，传入filter为groupid=该用户包含的其中一个设备分组groupid后23位，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupid%22%3A%20%22"+ self.user_0['device_groups'][0]['groupid'][1:23] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,500)
#     def test_get_device_groups_agent_filter_groupid_22(self):
#         '''登录代理商，传入filter为groupid=该用户包含的其中一个设备分组groupid中间22位，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupid%22%3A%20%22"+ self.user_0['device_groups'][0]['groupid'][1:22] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,500)
#     def test_get_device_groups_agent_filter_groupid_of_other_user(self):
#         '''登录代理商，传入filter为groupid=其他代理商包含的其中一个设备分组groupid，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupid%22%3A%20%22"+ self.users_device_groups_arr_2[1]['device_groups'][0]['groupid'] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_filter_groupid_not_exist(self):
#         '''登录代理商，传入filter为groupid=不存在的设备分组groupid，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupid%22%3A%20%22"+ 'a0b1c2d3e4g5r6w7f8d9f0g1' + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,500)
#     def test_get_device_groups_agent_filter_desc_right(self):
#         '''登录代理商，传入filter为desc=该用户包含的其中一个设备分组desc，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22desc%22%3A%20%22"+ self.user_0['device_groups'][0]['desc'] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,self.user_0['device_groups'][:-1])
#     def test_get_device_groups_agent_filter_desc_ls_1(self):
#         '''登录代理商，传入filter为desc=该用户包含的其中一个设备分组desc少一位，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22desc%22%3A%20%22"+ self.user_0['device_groups'][0]['desc'][:-1] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_filter_desc_of_other_user(self):
#         '''登录代理商，传入filter为desc=其他用户包含的其中一个设备分组desc，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22desc%22%3A%20%22"+ self.user_1['device_groups'][0]['desc'] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_filter_desc_not_exist(self):
#         '''登录代理商，传入filter为desc=不存在的一个设备分组desc，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22desc%22%3A%20%22"+ 'sgderthreth' + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_filter_owner_right(self):
#         '''登录代理商，传入filter为owner=该用户包含的其中一个设备分组username，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22owner%22%3A%20%22"+ self.user_0['username'] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,self.user_0['device_groups'])
#     def test_get_device_groups_agent_filter_owner_ls_1(self):    ###存在Bug
#         '''登录代理商，传入filter为owner=该用户包含的其中一个设备分组username少一位，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22owner%22%3A%20%22"+ self.user_0['username'][:-1] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_filter_owner_of_other_user(self):   ###存在Bug
#         '''登录代理商，传入filter为owner=其他用户包含的其中一个设备分组username，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22owner%22%3A%20%22"+ self.user_1['username'] + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_filter_owner_not_exist(self):   ###存在Bug
#         '''登录代理商，传入filter为owner=不存在的一个设备分组username，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22owner%22%3A%20%22"+ 'sgderthreth' + "%22%7D" ,"","","",1)
#         self.assertEqual(self.result,[])
#     # def test_get_device_groups_agent_filter_created_time_right(self):
#     #     '''登录代理商，传入filter为created_time=该用户包含的其中一个设备分组created_time，判断返回status_code和body内容'''
#     #     self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22created_time%22%3A"+ str(self.user_0['device_groups'][0]['created_time']) + "%7D","","","",1)
#     #     if self.user_0['device_groups'][0]['created_time'] == self.user_0['device_groups'][1]['created_time']:
#     #         result = self.user_0['device_groups']
#     #     else:
#     #         result = self.user_0['device_groups'][:-1]
#     #     self.assertEqual(self.result,result)
#     # def test_get_device_groups_agent_filter_created_time_ls_1(self):
#     #     '''登录代理商，传入filter为created_time=该用户包含的其中一个设备分组created_time少一位，判断返回status_code和body内容'''
#     #     self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22created_time%22%3A"+ str(self.user_0['device_groups'][0]['created_time'])[:-1] + "%7D" ,"","","",1)
#     #     self.assertEqual(self.result,[])
#     # def test_get_device_groups_agent_filter_created_time_of_other_user(self):
#     #     '''登录代理商，传入filter为created_time=其他用户包含的其中一个设备分组created_time，判断返回status_code和body内容'''
#     #     self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22created_time%22%3A"+ str(self.user_1['device_groups'][0]['created_time']) + "%7D","","","",1)
#     #     if self.user_0['device_groups'][0]['created_time'] == self.user_0['device_groups'][1]['created_time']:
#     #         result = self.user_0['device_groups']
#     #     else:
#     #         result = self.user_0['device_groups'][1:]
#     #     self.assertEqual(self.result,result)
#     # def test_get_device_groups_agent_filter_created_time_not_exist(self):
#     #     '''登录代理商，传入filter为created_time=不存在的一个设备分组created_time，判断返回status_code和body内容'''
#     #     self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22created_time%22%3A%20"+ '1534888511' + "%7D" ,"","","",1)
#     #     self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_skip_0(self):
#         '''登录代理商，传入skip=0，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=0","","",1)
#         self.assertEqual(self.result,self.agent1_device_groups_arr)
#     def test_get_device_groups_agent_skip_1(self):
#         '''登录代理商，传入skip=1，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=1","","",1))
#         self.assertEqual(self.result,3)
#     def test_get_device_groups_agent_skip_2(self):
#         '''登录代理商，传入skip=2，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=2","","",1))
#         self.assertEqual(self.result,2)
#     def test_get_device_groups_agent_skip_3(self):
#         '''登录代理商，传入skip=3，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=3","","",1))
#         self.assertEqual(self.result,1)
#     def test_get_device_groups_agent_skip_4(self):
#         '''登录代理商，传入skip=4，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=4","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_skip_special_char(self):    ##存在Bug
#         '''登录代理商，传入skip=特殊字符，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=**&&((","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_skip_chinese_char(self):    ##存在Bug
#         '''登录代理商，传入skip=中文字符，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=中文字符","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_skip_english_char(self):    ##存在Bug
#         '''登录代理商，传入skip=英文字符，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=sdgfg","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_limit_0(self):
#         '''登录代理商，传入limit=0，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"","limit=0","",1)
#         self.assertEqual(self.result,self.agent1_device_groups_arr)
#     def test_get_device_groups_agent_limit_1(self):
#         '''登录代理商，传入limit=1，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"","limit=1","",1))
#         self.assertEqual(self.result,1)
#     def test_get_device_groups_agent_limit_2(self):
#         '''登录代理商，传入limit=2，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"","limit=2","",1))
#         self.assertEqual(self.result,2)
#     def test_get_device_groups_agent_limit_3(self):
#         '''登录代理商，传入limit=3，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"","limit=3","",1))
#         self.assertEqual(self.result,3)
#     def test_get_device_groups_agent_limit_4(self):
#         '''登录代理商，传入limit=4，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"","limit=4","",1))
#         self.assertEqual(self.result,4)
#     def test_get_device_groups_agent_limit_special_char(self):   ##存在Bug
#         '''登录代理商，传入limit=特殊字符，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"","limit=**&&((","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_limit_chinese_char(self):   ##存在Bug
#         '''登录代理商，传入limit=中文字符，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"","limit=中文字符","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_limit_english_char(self):   ##存在Bug
#         '''登录代理商，传入limit=英文字符，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"","limit=sdgfg","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_aggregation_count(self):
#         '''登录代理商，传入aggregation=count，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"","","aggregation=count",1)
#         self.assertEqual(self.result,4)
#     def test_get_device_groups_agent_groupname_skip_0(self):
#         '''登录代理商，传入filter=该用户包含的一个设备分组groupname和skip=0，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"&skip=0","","",1)
#         self.assertEqual(self.result,self.user_0['device_groups'][:-1])
#     def test_get_device_groups_agent_groupname_skip_1(self):
#         '''登录代理商，传入filter=该用户包含的一个设备分组groupname和skip=1，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"&skip=1","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_groupname_skip_2(self):
#         '''登录代理商，传入filter=该用户包含的一个设备分组groupname和skip=2，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"&skip=2","","",1)
#         self.assertEqual(self.result,[])
#     def test_get_device_groups_agent_groupname_limit_0(self):
#         '''登录代理商，传入filter=该用户包含的一个设备分组groupname和limit=0，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"","&limit=0","",1)
#         self.assertEqual(self.result,self.user_0['device_groups'][:-1])
#     def test_get_device_groups_agent_groupname_limit_1(self):
#         '''登录代理商，传入filter=该用户包含的一个设备分组groupname和limit=1，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"","&limit=1","",1)
#         self.assertEqual(self.result,self.user_0['device_groups'][:-1])
#     def test_get_device_groups_agent_groupname_limit_2(self):
#         '''登录代理商，传入filter=该用户包含的一个设备分组groupname和limit=2，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"","&limit=2","",1)
#         self.assertEqual(self.result,self.user_0['device_groups'][:-1])
#     def test_get_device_groups_agent_groupname_agrregation_aggregation(self):
#         '''登录代理商，传入filter=该用户包含的一个设备分组groupname和aggregation=count，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D" ,"","","&aggregation=count",1)
#         self.assertEqual(self.result,1)
#     def test_get_device_groups_agent_skip_0_limit_0(self):
#         '''登录代理商，传入skip=0，limit=0，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=0","&limit=0","",1)
#         self.assertEqual(self.result,self.agent1_device_groups_arr)
#     def test_get_device_groups_agent_skip_0_limit_1(self):
#         '''登录代理商，传入skip=0，limit=1，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=0","&limit=1","",1))
#         self.assertEqual(self.result,1)
#     def test_get_device_groups_agent_skip_0_limit_2(self):
#         '''登录代理商，传入skip=0，limit=1，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=0","&limit=2","",1))
#         self.assertEqual(self.result,2)
#     def test_get_device_groups_agent_skip_1_limit_0(self):
#         '''登录代理商，传入skip=1，limit=0，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=1","&limit=0","",1))
#         self.assertEqual(self.result,3)
#     def test_get_device_groups_agent_skip_1_limit_1(self):
#         '''登录代理商，传入skip=1，limit=1，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=1","&limit=1","",1))
#         self.assertEqual(self.result,1)
#     def test_get_device_groups_agent_skip_1_limit_2(self):
#         '''登录代理商，传入skip=1，limit=1，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=1","&limit=2","",1))
#         self.assertEqual(self.result,2)
#     def test_get_device_groups_agent_skip_2_limit_0(self):
#         '''登录代理商，传入skip=2，limit=0，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=2","&limit=0","",1))
#         self.assertEqual(self.result,2)
#     def test_get_device_groups_agent_skip_2_limit_1(self):
#         '''登录代理商，传入skip=2，limit=1，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=2","&limit=1","",1))
#         self.assertEqual(self.result,1)
#     def test_get_device_groups_agent_skip_2_limit_2(self):
#         '''登录代理商，传入skip=2，limit=1，判断返回status_code和body内容'''
#         self.result = len(get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"skip=2","&limit=2","",1))
#         self.assertEqual(self.result,2)
#     def test_get_device_groups_agent_limit_1_aggregation_count(self):
#         '''登录代理商，传入limit=1，aggregation=count，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"" ,"","limit=1","&aggregation=count",1)
#         self.assertEqual(self.result,4)
#     def test_get_device_groups_agent_groupname_skip_0_limit_0_aggregation_count(self):
#         '''登录代理商，传入filter=该用户包含的一个设备分组groupname，skip=0，limit=0，aggregation=count，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D"  ,"&skip=1","limit=1","&aggregation=count",1)
#         self.assertEqual(self.result,1)
#     def test_get_device_groups_agent_groupname_skip_1_limit_1_aggregation_count(self):
#         '''登录代理商，传入filter=该用户包含的一个设备分组groupname，skip=0，limit=0，aggregation=count，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D"  ,"&skip=1","limit=1","&aggregation=count",1)
#         self.assertEqual(self.result,1)
#     def test_get_device_groups_agent_groupname_skip_1_limit_0_aggregation_count(self):
#         '''登录代理商，传入filter=该用户包含的一个设备分组groupname，skip=0，limit=0，aggregation=count，判断返回status_code和body内容'''
#         self.result = get_device_groups_test(self.base_url,self.agents_orgnizations_users_device_groups[0],"filter=%7B%22groupname%22%3A%20%22"+ self.user_0['device_groups'][0]['groupname'] + "%22%7D"  ,"&skip=1","limit=0","&aggregation=count",1)
#         self.assertEqual(self.result,1)

if __name__ == '__main__':
    unittest.main()