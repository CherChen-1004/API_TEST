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

def get_device_data_test(url,login_user,devtype,devid,filter,descend,skip,limit,starttime,endtime,aggregation,login_or_not):
    '''参数化编程，agent_or_user：，login_or_not:是否登录，默认登录'''
    if (devtype == "" and devid == "" and filter == "" and descend == "" and skip == "" and limit == "" and starttime == "" and endtime == "" and aggregation == "") == True:
        base_url = url
    else:
        base_url = url + "/" + devid + "/data?" + devtype + filter + descend + skip + limit + starttime + endtime + aggregation
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
            return r.json()['data']
        else:
            return r.json()['count']
    else:
        return r.status_code
device_data_arr = ["total_energy","today_energy","temperature","gfci","bus_volt","power","q_power","pf","pv1_volt","pv1_curr","pv2_volt","pv2_curr","pv3_volt","pv3_curr","l1_volt","l1_curr","l1_freq","l1_dci","l1_power","l1_pf"]
class DeviceDataGetTest(unittest.TestCase):
    '''查询满足条件的设备数据 接口测试'''
    '''创建一组普通用户，创建两组设备，一组用于普通用户创建设备分组后添加，一组可自由测试'''
    @classmethod
    def setUpClass(cls):
        global uers_device_groups_devices_datas_arr,TestData
        TestData = InitialData(73, 73, 73,75)
        uers_device_groups_devices_datas_arr = TestData.users_device_groups_devices_datas(2,2,3)

    def setUp(self):
        global users_device_groups_devices_datas_arr
        self.base_url = "https://zlab.zlgcloud.com:443/v1/devices"
        self.users_device_groups_devices_datas_arr = uers_device_groups_devices_datas_arr
        self.user_0 = self.users_device_groups_devices_datas_arr[0]
        self.user_1 = self.users_device_groups_devices_datas_arr[1]
        self.user_0_device_group_0 = self.user_0['device_groups'][0]
        self.user_0_device_group_1 = self.user_0['device_groups'][1]
        self.user_1_device_group_0 = self.user_1['device_groups'][0]
        self.user_1_device_group_1 = self.user_1['device_groups'][1]
        # print(self.user_1_device_group_0['devices'][0])
    def tearDown(self):
        print(self.result)

    @classmethod
    def tearDownClass(cls):
        global users_device_groups_devices_datas_arr,TestData
        TestData.delete_all_devices_and_data()
        TestData.delete_all_users()

    def test_get_device_data_devtype_right_devid_right(self):
        ''' 登录普通用户，传入该用户包含的设备的devtype和devid'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","","","","","",1)
        self.result.sort(key=str)
        datas_arr = self.user_0_device_group_0['devices'][0]['data'][0:]
        datas_arr.sort(key=str)
        print(datas_arr)
        self.assertEqual(self.result, datas_arr)
    def test_get_device_data_devtype_right_devid_ls_1(self):
        ''' 登录普通用户，传入该用户包含的设备的devtype和devid少一位字符'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'][:-1],
                                           "","","","","","","",1)
        self.assertEqual(self.result, 404)
    def test_get_device_data_devtype_right_devid_not_exist(self):
        ''' 登录普通用户，传入该用户包含的设备的devtype和d不存在的devid'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],"sgfwetsdf",
                                           "","","","","","","",1)
        self.assertEqual(self.result, 404)
    def test_get_device_data_devtype_right_devid_of_other_user(self):
        ''' 登录普通用户，传入该用户包含的设备的devtype和其他用户包含的设备的devid'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "","","","","","","",1)
        self.assertEqual(self.result, 403)
    def test_get_device_data_devid_right_devtype_ls_1(self):
        ''' 登录普通用户，传入该用户包含的设备的devid和devtype少一位字符'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'][:-1],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","","","","","",1)
        self.assertEqual(self.result, 400)
    def test_get_device_data_devid_right_devtype_not_exist(self):
        ''' 登录普通用户，传入该用户包含的设备的devid和不存在的devtype'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + 'gedryxfvsr5',self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","","","","","",1)
        self.assertEqual(self.result, 400)



    def test_get_device_data_filter_device_data_arr_0(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[0] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        print('expect value:',self.user_0_device_group_0['devices'][0]['data'][0:1])
        self.assertEqual(self.result, self.user_0_device_group_0['devices'][0]['data'][0:1])
    def test_get_device_data_filter_device_data_arr_1(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"&descend=false","","","","","",1)

        self.assertEqual(self.result, self.user_0_device_group_0['devices'][0]['data'][0:2])
    def test_get_device_data_filter_device_data_arr_2(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[2] + "%22%3A0%7D" ,"&descend=false","","","","","",1)

        self.assertEqual(self.result, self.user_0_device_group_0['devices'][0]['data'][1:])
    def test_get_device_data_filter_device_data_arr_3(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[3] + "%22%3A0%7D" ,"&descend=false","","","","","",1)

        self.assertEqual(self.result, self.user_0_device_group_0['devices'][0]['data'][2:])



    def test_get_device_data_filter_device_data_arr_4(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[4] + "%22%3A0%7D" ,"&descend=false","","","","","",1)

        self.assertEqual(self.result, [])
    def test_get_device_data_filter_device_data_arr_4_1(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][1]['devtype'],self.user_0_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[4] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][1]['data'][0:2])
    def test_get_device_data_filter_device_data_arr_5(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][1]['devtype'],self.user_0_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[5] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][1]['data'][1:])
    def test_get_device_data_filter_device_data_arr_6(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][1]['devtype'],self.user_0_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[6] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][1]['data'][2:])
    def test_get_device_data_filter_device_data_arr_7(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][0]['devtype'],self.user_0_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[7] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_0_device_group_1['devices'][0]['data'][0:2])
    def test_get_device_data_filter_device_data_arr_8(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][0]['devtype'],self.user_0_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[8] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_0_device_group_1['devices'][0]['data'][1:])
    def test_get_device_data_filter_device_data_arr_9(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][0]['devtype'],self.user_0_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[9] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_0_device_group_1['devices'][0]['data'][2:])
    def test_get_device_data_filter_device_data_arr_10(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][1]['devtype'],self.user_0_device_group_1['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[10] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_0_device_group_1['devices'][1]['data'][0:2])
    def test_get_device_data_filter_device_data_arr_11(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][1]['devtype'],self.user_0_device_group_1['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[11] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_0_device_group_1['devices'][1]['data'][1:])
    def test_get_device_data_filter_device_data_arr_12(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][1]['devtype'],self.user_0_device_group_1['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[12] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_0_device_group_1['devices'][1]['data'][2:])
    def test_get_device_data_filter_device_data_arr_13(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[13] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_1_device_group_0['devices'][0]['data'][0:2])
    def test_get_device_data_filter_device_data_arr_14(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[14] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_1_device_group_0['devices'][0]['data'][1:])
    def test_get_device_data_filter_device_data_arr_15(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[15] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_1_device_group_0['devices'][0]['data'][2:])
    def test_get_device_data_filter_device_data_arr_16(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_0['devices'][1]['devtype'],self.user_1_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[16] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_1_device_group_0['devices'][1]['data'][0:2])
    def test_get_device_data_filter_device_data_arr_17(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_0['devices'][1]['devtype'],self.user_1_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[17] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_1_device_group_0['devices'][1]['data'][1:])
    def test_get_device_data_filter_device_data_arr_18(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = get_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_1['devices'][0]['devtype'],self.user_1_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[18] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.assertEqual(self.result,self.user_1_device_group_1['devices'][0]['data'][0:1])
    def test_get_device_data_descend_false(self):
        ''' 登录普通用户，传入descend=false'''
        result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","","","",1)
        self.result = result[0]['time'] <= result[1]['time'] <= result[2]['time']
        self.assertEqual(self.result, True)
    def test_get_device_data_descend_true(self):
        ''' 登录普通用户，传入该用户包含的设备的devtype和devid,descend=1s'''
        result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=true","","","","","",1)
        self.result = result[0]['time'] >= result[1]['time'] >= result[2]['time']
        self.assertEqual(self.result, True)
    def test_get_device_data_skip_0(self):
        ''' 不登陆，传入skip=0'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&skip=0","","","","",1))
        self.assertEqual(self.result, 3)
    def test_get_device_data_skip_1(self):
        ''' 登录普通用户，传入skip=1'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&skip=1","","","","",1))
        self.assertEqual(self.result, 2)
    def test_get_device_data_skip_2(self):
        ''' 登录普通用户，传入skip=2'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&skip=2","","","","",1))
        self.assertEqual(self.result, 1)
    def test_get_device_data_skip_3(self):
        ''' 登录普通用户，传入skip=3'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&skip=3","","","","",1))
        self.assertEqual(self.result, 0)
    def test_get_device_data_skip_4(self):
        ''' 登录普通用户，传入skip=3'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&skip=4","","","","",1))
        self.assertEqual(self.result, 0)
    def test_get_device_data_skip_special_char(self):
        ''' 登录普通用户，传入skip=其他字符'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&skip=e6qw","","","","",1)
        self.assertEqual(self.result, 400)
    def test_get_device_data_limit_0(self):
        ''' 登录普通用户，传入limit=0'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&limit=0","","","","",1))
        self.assertEqual(self.result, 3)
    def test_get_device_data_limit_1(self):
        ''' 登录普通用户，传入limit=1'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&limit=1","","","","",1))
        self.assertEqual(self.result, 1)
    def test_get_device_data_limit_2(self):
        ''' 登录普通用户，传入limit=2'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&limit=2","","","","",1))
        self.assertEqual(self.result, 2)
    def test_get_device_data_limit_3(self):
        ''' 登录普通用户，传入limit=3'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&limit=3","","","","",1))
        self.assertEqual(self.result, 3)
    def test_get_device_data_limit_4(self):
        ''' 登录普通用户，传入limit=3'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&limit=4","","","","",1))
        self.assertEqual(self.result, 3)
    def test_get_device_data_limit_special_char(self):
        ''' 登录普通用户，传入limit=其他字符'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","&limit=456dfgh","","","","",1)
        self.assertEqual(self.result, 400)
    def test_get_device_data_starttime_0(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","&starttime=","","",1)
        self.result.sort(key=str)
        datas_arr = self.user_0_device_group_0['devices'][0]['data'][0:]
        datas_arr.sort(key=str)
        print(datas_arr)
        self.assertEqual(self.result, datas_arr)
    def test_get_device_data_starttime_10000(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","&starttime=10000","","",1)
        self.result.sort(key=str)
        datas_arr = self.user_0_device_group_0['devices'][0]['data'][0:]
        datas_arr.sort(key=str)
        print('dddddddddd',datas_arr)
        self.assertEqual(self.result, datas_arr)




    def test_get_device_data_starttime_10001(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","&starttime=10001","","",1)

        self.assertEqual(self.result, self.user_0_device_group_0['devices'][0]['data'][1:])
    def test_get_device_data_starttime_10002(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","&starttime=10002","","",1)
        self.result.sort(key=str)
        expect_result = self.user_0_device_group_0['devices'][0]['data'][2:][0:]
        expect_result.sort(key=str)
        self.assertEqual(self.result, expect_result)



    def test_get_device_data_starttime_10003(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","&starttime=10003","","",1)
        self.assertEqual(self.result, [])
    def test_get_device_data_endtime_0(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","","&endtime=0","",1)
        self.assertEqual(self.result, [])
    def test_get_device_data_endtime_10000(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","","&endtime=10000","",1)
        self.assertEqual(self.result, self.user_0_device_group_0['devices'][0]['data'][0:1])
    def test_get_device_data_endtime_10001(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","","&endtime=10001","",1)
        self.assertEqual(self.result, self.user_0_device_group_0['devices'][0]['data'][0:2])
    def test_get_device_data_endtime_10002(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","","&endtime=10002","",1)
        self.assertEqual(self.result, self.user_0_device_group_0['devices'][0]['data'])
    def test_get_device_data_aggregation_count(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","","","","","&aggregation=count",1)
        self.assertEqual(self.result, 3)
    def test_get_device_data_filter_descend_true(self):
        ''' 登录普通用户，传入descend=true'''
        result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"&descend=true","","","","","",1)
        self.result = result[0]['time'] >= result[1]['time']
        self.assertEqual(self.result, True)
    def test_get_device_data_filter_descend_false(self):
        ''' 登录普通用户，传入descend=false'''
        result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"&descend=false","","","","","",1)
        self.result = result[0]['time'] <= result[1]['time']
        self.assertEqual(self.result, True)
    def test_get_device_data_filter_skip_0(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和skip=0'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","&skip=0","","","","",1))
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_skip_1(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和skip=1'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","&skip=1","","","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_data_filter_skip_2(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和skip=2'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","&skip=2","","","","",1))
        self.assertEqual(self.result,0)
    def test_get_device_data_filter_limit_0(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和limit=0'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","&limit=0","","","","",1))
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_limit_1(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和limit=1'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","&limit=1","","","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_data_filter_limit_2(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和limit=2'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","&limit=2","","","","",1))
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_starttime_0(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和limit=3'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","","","&starttime=0","","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][0]['data'][0:2])
    def test_get_device_data_filter_starttime_10001(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和starttime=10001'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","","","&starttime=10001","","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][0]['data'][1:2])
    def test_get_device_data_filter_endtime_0(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和endtime=0'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","","","&endtime=0","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_data_filter_endtime_10001(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和endtime=10001'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","","","&endtime=10001","","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][0]['data'][0:2])
    def test_get_device_data_filter_aggregation(self):
        ''' 登录普通用户，传入filter=该用户包含的数据段和aggregation=0'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"","","","","","&aggregation=count",1)
        self.assertEqual(self.result,2)
    def test_get_device_data_skip_0_limit_0(self):
        ''' 登录普通用户，传入skip=0和limit=0'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&skip=0","&limit=0","","","",1))
        self.assertEqual(self.result,3)
    def test_get_device_data_skip_1_limit_0(self):
        ''' 登录普通用户，传入skip=1和limit=0'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&skip=1","&limit=0","","","",1))
        self.assertEqual(self.result,2)
    def test_get_device_data_skip_1_limit_1(self):
        ''' 登录普通用户，传入skip=1和limit=1'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&skip=1","&limit=1","","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_data_skip_1_starttime_10001(self):
        ''' 登录普通用户，传入skip=1和startime=10001'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&skip=1","","&starttime=10001","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_data_skip_1_starttime_10002(self):
        ''' 登录普通用户，传入skip=1和startime=10002'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&skip=1","","&starttime=10002","","",1))
        self.assertEqual(self.result,0)
    def test_get_device_data_skip_1_endtime_10001(self):
        ''' 登录普通用户，传入skip=1和endtime=10001'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&skip=1","","","&endtime=10001","",1))
        self.assertEqual(self.result,1)
    def test_get_device_data_skip_1_endtime_10002(self):
        ''' 登录普通用户，传入skip=1和endtime=10002'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&skip=1","","","&endtime=10002","",1))
        self.assertEqual(self.result,2)
    def test_get_device_data_skip_1_aggregation_count(self):
        ''' 登录普通用户，传入skip=1和aggregation=count'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&skip=1","","","","&aggregation=count",1)
        self.assertEqual(self.result,3)
    def test_get_device_data_limit_1_starttime_10001(self):
        ''' 登录普通用户，传入skip=1和starttime=10001'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&limit=1","","&starttime=10001","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_data_limit_0_starttime_10002(self):
        ''' 登录普通用户，传入skip=1和starttime=10002'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&limit=1","","&starttime=10002","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_data_limit_1_endtime_10001(self):
        ''' 登录普通用户，传入limit=1和starttime=10001'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&limit=1","","","&endtime=10001","",1))
        self.assertEqual(self.result,1)
    def test_get_device_data_limit_3_endtime_10000(self):
        ''' 登录普通用户，传入limit=3和starttime=10000'''
        self.result = len(get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&limit=1","","","&endtime=10000","",1))
        self.assertEqual(self.result,1)
    def test_get_device_data_limit_1_aggregation_count(self):
        ''' 登录普通用户，传入limit=1和aggregation=count'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "" ,"","&limit=1","","","","&aggregation=count",1)
        self.assertEqual(self.result,3)
    def test_get_device_data_starttime_0_endtime_0(self):
        ''' 登录普通用户，传入starttime=0和endtime=0'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","&starttime=0","&endtime=0","",1)
        self.assertEqual(self.result, [])
    def test_get_device_data_starttime_10000_endtime_10001(self):
        ''' 登录普通用户，传入starttime=该用户包含的设备的第一个时间'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","&starttime=10000","&endtime=10001","",1)
        self.assertEqual(self.result,self.user_0_device_group_0['devices'][0]['data'][0:2])
    def test_get_device_data_starttime_10000_endtime_10001_aggregation_count(self):
        ''' 登录普通用户，传入starttime=10000、endtime=10001和aggregation=count'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","&descend=false","","","&starttime=10000","&endtime=10001","&aggregation=count",1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_descend_true_skip_1_limit_1(self):
        ''' 登录普通用户，传入filter、descend=true，skip=1，limit=1'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,"&descend=true","&skip=1","&limit=1","","","",1)[0]['time']
        self.assertEqual(self.result, 10000)
    def test_get_device_data_not_login(self):
        ''' 不登录，传入该用户包含的设备的devtype和devid'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","","","","","",0)
        self.assertEqual(self.result, 401)
    def test_get_device_data_logout(self):
        ''' 登录后再退出，传入该用户包含的设备的devtype和devid'''
        self.result = get_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "","","","","","","",2)
        self.assertEqual(self.result, 401)

if __name__ == '__main__':
    for n in range(73,75):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()