# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.test_data import device_data_arr

'''返回码如下：
            200	操作成功
            401	没有登录
            404 设备分组不存在
            500	服务器错误'''

def update_device_data_test(url,login_user,devtype,devid,filter,data,login_or_not=1):
    '''参数化编程，agent_or_user：登录代理商/普通用户=1/0，user_agent：传入的代理商/普通用户，login_or_not:是否登录，默认登录'''
    base_url = url + devid + '/data?devtype=' + devtype +filter
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]), session)
    if login_or_not == 1:
        user.login()
        r = session.put(base_url,json=data)
    elif login_or_not == 0:
        r = requests.put(base_url,json=data)
    else:
        user.login()
        user.logout()
        r = session.put(base_url,json=data)
    if r.status_code == 200:
        return r.json()['data']
    return r.status_code

class DevicesDataUpdateTest(unittest.TestCase):
    '''批量更新设备数据 接口测试'''

    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/devices/"
        self.TestData = InitialData(75, 75, 75,77)
        self.users_device_groups_devices_datas_arr = self.TestData.users_device_groups_devices_datas(2,2,3)
        self.user_0 = self.users_device_groups_devices_datas_arr[0]
        self.user_1 = self.users_device_groups_devices_datas_arr[1]
        self.user_0_device_group_0 = self.user_0['device_groups'][0]
        self.user_0_device_group_1 = self.user_0['device_groups'][1]
        self.user_1_device_group_0 = self.user_1['device_groups'][0]
        self.user_1_device_group_1 = self.user_1['device_groups'][1]
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_devices_and_data()
        self.TestData.delete_all_users()
    def test_update_device_data_right(self):
        '''登录普通用户，传入改用户所属设备的devtype和devid，filter为空，data为time=0'''
        data= {"time": 0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result, {"n":3,"nModified":3,"ok":1})
    def test_update_device_data_devtype_ls_1(self):
        '''登录普通用户，传入改用户所属设备的devtype少一位字符和devid，filter为空，data为time=0'''
        data= {"time": 0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'][:-1],self.user_0_device_group_0['devices'][0]['devid'],"" ,data,1)
        self.assertEqual(self.result, 400)
    def test_update_device_data_devtype_wrong(self):
        '''登录普通用户，传入改用户所属设备的devtype错误和devid，filter为空，data为time=0'''
        data= {"time": 0}
        self.result = update_device_data_test(self.base_url,self.user_0,"dsffffg",self.user_0_device_group_0['devices'][0]['devid'],"" ,data,1)
        self.assertEqual(self.result, 400)
    def test_update_device_data_devid_ls_1(self):
        '''登录普通用户，传入改用户所属设备的devtype和devid少一位，filter为空，data为time=0'''
        data= {"time": 0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'][:-1],"",data,1)
        self.assertEqual(self.result, 404)
    def test_update_device_data_devid_wrong(self):
        '''登录普通用户，传入改用户所属设备的devtype和devid少一位，filter为空，data为time=0'''
        data= {"time": 0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],"sgghdfg","",data,1)
        self.assertEqual(self.result, 404)
    def test_update_device_data_devid_of_other_user(self):
        '''登录普通用户，传入改用户所属设备的devtype，devid为其他用户所属设备，filter为空，data为time=0'''
        data= {"time": 0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result, 403)

    def test_get_device_data_filter_device_data_arr_0(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[0] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result, {"n":1,"nModified":1,"ok":1})
    def test_get_device_data_filter_device_data_arr_1(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result, {"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_2(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[2] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result, {"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_3(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[3] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result, {"n":1,"nModified":1,"ok":1})
    def test_get_device_data_filter_device_data_arr_4(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[4] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result, {"n":0,"nModified":0,"ok":1})
    def test_get_device_data_filter_device_data_arr_4_1(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][1]['devtype'],self.user_0_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[4] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_5(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][1]['devtype'],self.user_0_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[5] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_6(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][1]['devtype'],self.user_0_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[6] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":1,"nModified":1,"ok":1})
    def test_get_device_data_filter_device_data_arr_7(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_1['devices'][0]['devtype'],self.user_0_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[7] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_8(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_1['devices'][0]['devtype'],self.user_0_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[8] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_9(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_1['devices'][0]['devtype'],self.user_0_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[9] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":1,"nModified":1,"ok":1})
    def test_get_device_data_filter_device_data_arr_10(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_1['devices'][1]['devtype'],self.user_0_device_group_1['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[10] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_11(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_1['devices'][1]['devtype'],self.user_0_device_group_1['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[11] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_12(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_1['devices'][1]['devtype'],self.user_0_device_group_1['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[12] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":1,"nModified":1,"ok":1})
    def test_get_device_data_filter_device_data_arr_13(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_1,self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[13] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_14(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_1,self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[14] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_15(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_1,self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[15] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":1,"nModified":1,"ok":1})
    def test_get_device_data_filter_device_data_arr_16(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_1,self.user_1_device_group_0['devices'][1]['devtype'],self.user_1_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[16] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_17(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_1,self.user_1_device_group_0['devices'][1]['devtype'],self.user_1_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[17] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":2,"nModified":2,"ok":1})
    def test_get_device_data_filter_device_data_arr_18(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_1,self.user_1_device_group_1['devices'][0]['devtype'],self.user_1_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[18] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result,{"n":1,"nModified":1,"ok":1})
    def test_get_device_data_filter_data_ls_1(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        data={"time":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1][:-1] + "%22%3A0%7D" ,data, 1)
        self.assertEqual(self.result, {"n":0,"nModified":0,"ok":1})
    def test_get_device_data_not_login(self):
        ''' 不登录，传入该用户包含的设备的数据'''
        data = {"time": 0}
        self.result = update_device_data_test(self.base_url,self.user_1,self.user_1_device_group_1['devices'][0]['devtype'],self.user_1_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[18] + "%22%3A0%7D" ,data,0)
        self.assertEqual(self.result,401)
    def test_get_device_data_logout(self):
        ''' 登录后退出，传入该用户包含的设备的数据'''
        data = {"time": 0}
        self.result = update_device_data_test(self.base_url,self.user_1,self.user_1_device_group_1['devices'][0]['devtype'],self.user_1_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[18] + "%22%3A0%7D" ,data,2)
        self.assertEqual(self.result,401)
    def test_update_device_data_total_energy_right(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入total_energy'''
        data = {"total_energy":12}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_total_energy_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入total_energy少一位字符'''
        data = {"total_energ":0}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_total_energy_char(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入total_energy为错误类型'''
        data = {"total_energ":'0'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_temperature(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature'''
        data = {"temperature":45}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_temperture_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature少一位字符'''
        data = {"today_energ":34}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_today_energy_char(self):       ###存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature为字符串类型'''
        data = {"temperature":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_temperature_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature少一位字符'''
        data = {"temperatur":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_temperature_char(self):   #存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature为字符串类型'''
        data = {"temperature":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_gfci(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入gfci'''
        data = {"gfci":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_gfci_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入gfci少一位字符'''
        data = {"gfc":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_gfci_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入gfci为字符串类型'''
        data = {"gfci":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_gfci_0(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入gfci为0'''
        data = {"gfci":23}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_power(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入power'''
        data = {"power":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_power_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入power少一位字符'''
        data = {"powe":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_power_char(self):     ##存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入power为字符串类型'''
        data = {"power":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_bus_volt(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入bud_volt'''
        data = {"bus_volt":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_bus_volt_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入bud_volt少一位字符'''
        data = {"bud_vol":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_bus_volt_char(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入bud_volt为字符串类型'''
        data = {"bud_volt":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_q_power(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入q_power'''
        data = {"q_power":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_q_power_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入q_power少一位字符'''
        data = {"q_powe":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_q_power_char(self):   ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入q_power为字符串类型'''
        data = {"q_power":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_pf(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pf'''
        data = {"pf":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_pf_char(self):        ##存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pf为字符串类型'''
        data = {"pf":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_pv1_volt(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv1_volt'''
        data = {"pv1_volt":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_pv1_volt_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv1_volt为字符串类型'''
        data = {"pv1_volt":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_pv1_curr(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv1_curr'''
        data = {"pv1_curr":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_pv1_curr_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv1_curr为字符串类型'''
        data = {"pv1_curr":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_pv2_volt(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv2_volt'''
        data = {"pv2_volt":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_pv2_volt_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv2_volt为字符串类型'''
        data = {"pv2_volt":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_pv3_volt(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv3_volt'''
        data = {"pv3_volt":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_pv3_volt_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv3_volt为字符串类型'''
        data = {"pv3_volt":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_pv3_curr(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv3_curr'''
        data = {"pv3_curr":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_pv3_curr_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv3_curr为字符串类型'''
        data = {"pv3_curr":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_l1_volt(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_volt'''
        data = {"l1_volt":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_l1_volt_char(self):   ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_volt为字符串类型'''
        data = {"l1_volt":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_l1_curr(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_curr'''
        data = {"l1_curr":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_l1_curr_char(self):   ##存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_curr为字符串类型'''
        data = {"l1_curr":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_l1_freq(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_freq'''
        data = {"l1_freq":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_l1_freq_char(self):   ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_freq为字符串类型'''
        data = {"l1_freq":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_l1_dci(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_dci'''
        data = {"l1_dci":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_l1_dci_char(self):    ##存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_dci为字符串类型'''
        data = {"l1_dci":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_l1_power(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_power'''
        data = {"l1_power":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_l1_power_char(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_power为字符串类型'''
        data = {"l1_power":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_l1_pf(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_pf'''
        data = {"l1_pf":15}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})
    def test_update_device_data_l1_pf_char(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_pf为字符串类型'''
        data = {"l1_pf":'ab'}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,400)
    def test_update_device_data_all(self):
        '''登录普通用户，传入所有的数据'''
        data = { "l1_pf":100, "total_energy":200,"temperature":12,"gfci":4654,"bus_volt":416,"power":4546,"q_power":135,"pf":546,"pv1_volt":154,"pv1_curr":132,"pv2_volt":451,"pv2_curr":465,"pv3_volt":654,"pv3_curr": 454,"l1_volt":4154,"l1_curr":468,"l1_freq": 4854,"l1_dci":465,"l1_power":454}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,1)
        self.assertEqual(self.result,{'nModified': 3, 'n': 3, 'ok': 1})
    def test_update_device_data_not_login(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_pf为字符串类型'''
        data = {"l1_pf":43}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,0)
        self.assertEqual(self.result,401)
    def test_update_device_data_logout(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_pf为字符串类型'''
        data = {"l1_pf":43}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"",data,2)
        self.assertEqual(self.result,401)
    def test_update_device_data_filter_right(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_pf为字符串类型'''
        data = {"l1_pf":4}
        self.result = update_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],"&filter=",data,1)
        self.assertEqual(self.result,{"n":3,"nModified":3,"ok":1})

if __name__ == '__main__':
    unittest.main()