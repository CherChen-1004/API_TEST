# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData

'''返回码如下：
            200	操作成功
            401	没有登录
            404 设备分组不存在
            500	服务器错误'''

def get_devices_test(url,user_agent,filter="",devtype="",skip="",limit="",aggregation="",login_or_not=1):
    '''参数化编程，agent_or_user：登录代理商/普通用户=1/0，user_agent：传入的代理商/普通用户，login_or_not:是否登录，默认登录'''
    if (filter == ''and devtype=="" and skip == '' and limit == '' and aggregation == '') == True:
        base_url = url
    else:
        base_url = url + '?' + filter + devtype +  skip + limit + aggregation
    session = requests.Session()
    num = int(user_agent['mobile'][-2:])
    user = UsersForTest(num, session)
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
        if aggregation != "":
            return r.json()['count']
        else:
            device_groups_data = r.json()['data']
            for device in device_groups_data:
                del device['time']
                del device['offlinetime']
                del device['registertime']
                del device['newfm']
                del device['onlinetime']
                del device['_id']
            device_groups_data.sort(key=str)
            return device_groups_data
    else:
        return r.status_code

class DeviceListInqueryTest(unittest.TestCase):
    '''查询设备列表 接口测试
    用例前提条件：创建两个普通用户，每个用户创建两个设备分组，每个分组添加两个设备'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/devices"
        self.TestData = InitialData(67, 67, 67,69)
        self.users_device_groups_devices_arr = self.TestData.users_device_groups_devices(2,2)
        self.user_0 = self.users_device_groups_devices_arr[0]
        self.user_1 = self.users_device_groups_devices_arr[1]
        self.user_0_device_group_0 = self.user_0['device_groups'][0]
        self.user_0_device_group_1 = self.user_0['device_groups'][1]
        self.user_1_device_group_0 = self.user_1['device_groups'][0]
        self.user_1_device_group_1 = self.user_1['device_groups'][1]
        # self.devices_list_of_agent_0 = self.user_0_device_group_0['devices'] + self.user_0_device_group_1['devices'] + self.user_1_device_group_0['devices'] + self.user_1_device_group_1['devices']
        self.devices_list_of_user_0 = self.user_0_device_group_0['devices'] + self.user_0_device_group_1['devices']
        # self.devices_list_of_agent_0.sort(key=str)
        # self.devices_list_of_user_0.sort(key=str)
    def tearDown(self):
        print(self.result)
        # self.TestData.delete_all_agents_and_orgnizations()
        self.TestData.delete_all_users()
    def test_devices_list_inquery_null(self):
        '''登录普通用户，传入参数为空'''
        self.result = get_devices_test(self.base_url,self.user_0,"","","","","",1)
        self.assertEqual(self.result,400)
    def test_devices_list_inquery_devtype_inverter(self):
        '''登录普通用户，传入devtype=inverter'''
        self.result = get_devices_test(self.base_url,self.user_0,"","devtype=inverter","","","",1)
        self.devices_list_of_user_0.sort(key=str)
        print('result:',self.result)
        print('expect result:',self.devices_list_of_user_0)
        self.assertEqual(self.result,self.devices_list_of_user_0)
    def test_devices_list_inquery_devid_right(self):
        '''登录普通用户，传入filter为devid=该用户包含的'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['devid'] + "%22%7D","&devtype=inverter","","","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][:-1])
    def test_devices_list_inquery_devid_ls_1(self):
        '''登录普通用户，传入filter为devid=该用户包含的少一位字符'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['devid'][:-1] + "%22%7D","&devtype=inverter","","","",1)
        self.assertEqual(self.result,[])
    def test_devices_list_inquery_devid_of_other_user(self):
        '''登录普通用户，传入filter为devid=其他用户包含的'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_1_device_group_0['devices'][0]['devid'] + "%22%7D","&devtype=inverter","","","",1)
        self.assertEqual(self.result,[])
    def test_devices_list_inquery_devid_null(self):
        '''登录普通用户，传入filter为devid=空字符串'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + '' + "%22%7D","&devtype=inverter","","","",1)
        self.assertEqual(self.result,[])
    def test_devices_list_inquery_model_right(self):
        '''登录普通用户，传入filter为model=该用户包含的'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22model%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['model'] + "%22%7D","&devtype=inverter","","","",1)
        self.devices_list_of_user_0.sort(key=str)
        print("result:",self.result)
        print('expect_result:',self.devices_list_of_user_0)
        self.assertEqual(self.result,self.devices_list_of_user_0)
    def test_devices_list_inquery_model_ls_1(self):
        '''登录普通用户，传入filter为model=该用户包含的少一位字符'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22model%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['model'][:-1] + "%22%7D","&devtype=inverter","","","",1)
        self.assertEqual(self.result,[])
    def test_devices_list_inquery_model_null(self):
        '''登录普通用户，传入filter为model=空字符串'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22model%22%3A%20%22" + '' + "%22%7D","&devtype=inverter","","","",1)
        self.assertEqual(self.result,[])

    def test_devices_list_inquery_owner_right(self):
        '''登录普通用户，传入filter为owner=该用户包含的'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","&devtype=inverter","","","",1)
        self.devices_list_of_user_0.sort(key=str)
        self.assertEqual(self.result,self.devices_list_of_user_0)
    def test_devices_list_inquery_owner_ls_1(self):     ##存在Bug
        '''登录普通用户，传入filter为owner=该用户包含的少一位字符'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'][:-1] + "%22%7D","&devtype=inverter","","","",1)
        self.assertEqual(self.result,400)
    def test_devices_list_inquery_owner_of_other_user(self):    ##存在Bug
        '''登录普通用户，传入filter为owner=其他用户包含的'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_1['username'] + "%22%7D","&devtype=inverter","","","",1)
        self.assertEqual(self.result,400)
    def test_devices_list_inquery_owner_null(self):             ##存在BUG
        '''登录普通用户，传入filter为owner=空字符串'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + '' + "%22%7D","&devtype=inverter","","","",1)
        self.devices_list_of_user_0.sort(key=str)
        print('reselt:',self.result)
        print('expect result:',self.devices_list_of_user_0)
        self.assertEqual(self.result,self.devices_list_of_user_0)

    def test_devices_list_inquery_skip_0(self):
        '''登录普通用户，传入skip=0'''
        self.result = get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&skip=0","","",1)
        self.devices_list_of_user_0.sort(key=str)
        print('result:',self.result)
        print('expect result:',self.devices_list_of_user_0)
        self.assertEqual(self.result,self.devices_list_of_user_0)
    def test_devices_list_inquery_skip_1(self):
        '''登录普通用户，传入skip=1'''
        self.result = len(get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&skip=1","","",1))
        self.devices_list_of_user_0.sort(key=str)
        self.assertEqual(self.result,3)
    def test_devices_list_inquery_skip_2(self):
        '''登录普通用户，传入skip=2'''
        self.result = len(get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&skip=2","","",1))
        self.assertEqual(self.result,2)
    def test_devices_list_inquery_skip_3(self):
        '''登录普通用户，传入skip=3'''
        self.result = len(get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&skip=3","","",1))
        self.assertEqual(self.result,1)
    def test_devices_list_inquery_skip_4(self):
        '''登录普通用户，传入skip=4'''
        self.result = len(get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&skip=4","","",1))
        self.assertEqual(self.result,0)
    def test_devices_list_inquery_limit_0(self):
        '''登录普通用户，传入limit=0'''
        self.result = get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&limit=0","","",1)
        self.devices_list_of_user_0.sort(key=str)
        print('result:',self.result)
        print('expect result:',self.devices_list_of_user_0)
        self.assertEqual(self.result,self.devices_list_of_user_0)
    def test_devices_list_inquery_limit_1(self):
        '''登录普通用户，传入limit=1'''
        self.result = len(get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&limit=1","","",1))
        self.assertEqual(self.result,1)
    def test_devices_list_inquery_limit_2(self):
        '''登录普通用户，传入limit=2'''
        self.result = len(get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&limit=2","","",1))
        self.assertEqual(self.result,2)
    def test_devices_list_inquery_limit_3(self):
        '''登录普通用户，传入limit=3'''
        self.result = len(get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&limit=3","","",1))
        self.assertEqual(self.result,3)
    def test_devices_list_inquery_limit_4(self):
        '''登录普通用户，传入limit=4'''
        self.result = len(get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&limit=4","","",1))
        self.assertEqual(self.result,4)
    def test_devices_list_inquery_limit_5(self):
        '''登录普通用户，传入limit=5'''
        self.result = len(get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","&limit=5","","",1))
        self.assertEqual(self.result,4)
    def test_devices_list_inquery_aggregation_count(self):
        '''登录普通用户，传入aggregation=count'''
        self.result = get_devices_test(self.base_url,self.user_0,'',"devtype=inverter","","","&aggregation=count",1)
        self.assertEqual(self.result,4)
    def test_devices_list_inquery_devid_skip_0(self):
        '''登录普通用户，传入devid为该用户包含的和skip=0'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['devid'] + "%22%7D","&devtype=inverter","&skip=0","","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][:-1])
    def test_devices_list_inquery_devid_skip_1(self):
        '''登录普通用户，传入devid为该用户包含的和skip=0'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['devid'] + "%22%7D","&devtype=inverter","&skip=1","","",1)
        self.assertEqual(self.result,[])
    def test_devices_list_inquery_devid_limit_0(self):
        '''登录普通用户，传入devid为该用户包含的和limit=0'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['devid'] + "%22%7D","&devtype=inverter","&limit=0","","",1)
        print('result:',self.result)
        print('expect result',self.user_0_device_group_0['devices'][:-1])
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][:-1])
    def test_devices_list_inquery_devid_limit_1(self):
        '''登录普通用户，传入devid为该用户包含的和limit=0'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['devid'] + "%22%7D","&devtype=inverter","&limit=1","","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][:-1])
    def test_devices_list_inquery_devid_aggregation_count(self):
        '''登录普通用户，传入devid为该用户包含的和aggregation=count'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['devid'] + "%22%7D","&devtype=inverter","","","&aggregation=count",1)
        self.assertEqual(self.result,1)
    def test_devices_list_inquery_devid_wrong_aggregation_count(self):
        '''登录普通用户，传入devid为非该用户包含的和aggregation=count'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + "sdgfsr" + "%22%7D","&devtype=inverter","","","&aggregation=count",1)
        self.assertEqual(self.result,0)
    def test_devices_list_inquery_skip_0_limit_0(self):
        '''登录普通用户，传入skip=0,limit=0'''
        self.result = get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=0","&limit=0","",1)
        self.devices_list_of_user_0.sort(key=str)
        self.assertEqual(self.result,self.devices_list_of_user_0)
    def test_devices_list_inquery_skip_0_limit_1(self):
        '''登录普通用户，传入skip=0,limit=1'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=0","&limit=1","",1))
        self.assertEqual(self.result,1)
    def test_devices_list_inquery_skip_0_limit_2(self):
        '''登录普通用户，传入skip=0,limit=2'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=0","&limit=2","",1))
        self.assertEqual(self.result,2)
    def test_devices_list_inquery_skip_0_limit_3(self):
        '''登录普通用户，传入skip=0,limit=3'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=0","&limit=3","",1))
        self.assertEqual(self.result,3)
    def test_devices_list_inquery_skip_0_limit_4(self):
        '''登录普通用户，传入skip=0,limit=4'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=0","&limit=4","",1))
        self.assertEqual(self.result,4)
    def test_devices_list_inquery_skip_1_limit_0(self):
        '''登录普通用户，传入skip=1,limit=0'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=1","&limit=0","",1))
        self.assertEqual(self.result,3)
    def test_devices_list_inquery_skip_1_limit_1(self):
        '''登录普通用户，传入skip=1,limit=1'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=1","&limit=1","",1))
        self.assertEqual(self.result,1)
    def test_devices_list_inquery_skip_1_limit_2(self):
        '''登录普通用户，传入skip=1,limit=2'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=1","&limit=2","",1))
        self.assertEqual(self.result,2)
    def test_devices_list_inquery_skip_1_limit_3(self):
        '''登录普通用户，传入skip=1,limit=3'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=1","&limit=3","",1))
        self.assertEqual(self.result,3)
    def test_devices_list_inquery_skip_1_limit_4(self):
        '''登录普通用户，传入skip=1,limit=4'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=1","&limit=4","",1))
        self.assertEqual(self.result,3)
    def test_devices_list_inquery_skip_2_limit_0(self):
        '''登录普通用户，传入skip=2,limit=0'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=2","&limit=0","",1))
        self.assertEqual(self.result,2)
    def test_devices_list_inquery_skip_2_limit_1(self):
        '''登录普通用户，传入skip=2,limit=1'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=2","&limit=1","",1))
        self.assertEqual(self.result,1)
    def test_devices_list_inquery_skip_2_limit_2(self):
        '''登录普通用户，传入skip=2,limit=2'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=2","&limit=2","",1))
        self.assertEqual(self.result,2)
    def test_devices_list_inquery_skip_2_limit_3(self):
        '''登录普通用户，传入skip=2,limit=3'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=2","&limit=3","",1))
        self.assertEqual(self.result,2)
    def test_devices_list_inquery_skip_2_limit_4(self):
        '''登录普通用户，传入skip=2,limit=4'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=2","&limit=4","",1))
        self.assertEqual(self.result,2)
    def test_devices_list_inquery_skip_3_limit_0(self):
        '''登录普通用户，传入skip=3,limit=0'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=3","&limit=0","",1))
        self.assertEqual(self.result,1)
    def test_devices_list_inquery_skip_3_limit_1(self):
        '''登录普通用户，传入skip=3,limit=1'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=3","&limit=1","",1))
        self.assertEqual(self.result,1)
    def test_devices_list_inquery_skip_3_limit_2(self):
        '''登录普通用户，传入skip=3,limit=2'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=3","&limit=2","",1))
        self.assertEqual(self.result,1)
    def test_devices_list_inquery_skip_4_limit_0(self):
        '''登录普通用户，传入skip=4,limit=0'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=4","&limit=0","",1))
        self.assertEqual(self.result,0)
    def test_devices_list_inquery_skip_4_limit_1(self):
        '''登录普通用户，传入skip=4,limit=1'''
        self.result = len(get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=4","&limit=1","",1))
        self.assertEqual(self.result,0)
    def test_devices_list_inquery_skip_0_aggregation_count(self):
        '''登录普通用户，传入skip=4,aggregation=count'''
        self.result = get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=4","","&aggregation=count",1)
        self.assertEqual(self.result,4)
    def test_devices_list_inquery_skip_4_aggregation_count(self):
        '''登录普通用户，传入skip=4,aggregation=count'''
        self.result = get_devices_test(self.base_url,self.user_0,"","devtype=inverter","&skip=4","","&aggregation=count",1)
        self.assertEqual(self.result,4)
    def test_devices_list_inquery_limit_0_aggregation_count(self):
        '''登录普通用户，传入limit=4,aggregation=count'''
        self.result = get_devices_test(self.base_url,self.user_0,"","devtype=inverter","","&limit=0","&aggregation=count",1)
        self.assertEqual(self.result,4)
    def test_devices_list_inquery_limit_2_aggregation_count(self):
        '''登录普通用户，传入limit=4,aggregation=count'''
        self.result = get_devices_test(self.base_url,self.user_0,"","devtype=inverter","","&limit=2","&aggregation=count",1)
        self.assertEqual(self.result,4)
    def test_devices_list_inquery_devid_skip_0_limit_0(self):
        '''登录普通用户，传入devid为该用户包含的和skip=0,limit=0'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['devid'] + "%22%7D","&devtype=inverter","&skip=0","&limit=0","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][:-1])
    def test_devices_list_inquery_devid_skip_1_limit_0(self):
        '''登录普通用户，传入devid为该用户包含的和和skip=1,limit=0'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['devid'] + "%22%7D","&devtype=inverter","&skip=1","&limit=0","",1)
        self.assertEqual(self.result,[])
    def test_devices_list_inquery_devid_skip_0_limit_0_aggregation_count(self):
        '''登录普通用户，传入devid为该用户包含的和和skip=0,limit=0,aggregation=count'''
        self.result = get_devices_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0_device_group_0['devices'][0]['devid'] + "%22%7D","&devtype=inverter","&skip=1","&limit=0","&aggregation=count",1)
        self.assertEqual(self.result,1)
##用设备分组的字段查询

if __name__ == '__main__':
    unittest.main()



