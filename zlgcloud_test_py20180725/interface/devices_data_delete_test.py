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

def delete_device_data_test(url,login_user,devtype,devid,filter,login_or_not):
    '''参数化编程，agent_or_user：，login_or_not:是否登录，默认登录'''
    if (devtype == "" and devid == "" and filter == "") == True:
        base_url = url
    else:
        base_url = url + "/" + devid + "/data?" + devtype + filter
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.delete(base_url)
    elif login_or_not == 0:
        r = requests.delete(base_url)
    else:
        user.login()
        user.logout()
        r = session.delete(base_url)
    if r.status_code == 200:
        return r.json()['data']['n']
    else:
        return r.status_code
device_data_arr = ["total_energy","today_energy","temperature","gfci","bus_volt","power","q_power","pf","pv1_volt","pv1_curr","pv2_volt","pv2_curr","pv3_volt","pv3_curr","l1_volt","l1_curr","l1_freq","l1_dci","l1_power","l1_pf"]
class DeviceDataDeleteTest(unittest.TestCase):
    '''删除设备数据 接口测试'''
    '''创建一组普通用户，创建两组设备，一组用于普通用户创建设备分组后添加，一组可自由测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/devices"
        self.TestData = InitialData(71, 71, 71,73)
        self.users_device_groups_devices_datas_arr = self.TestData.users_device_groups_devices_datas(2,2,3)
        self.user_0 = self.users_device_groups_devices_datas_arr[0]
        self.user_1 = self.users_device_groups_devices_datas_arr[1]
        self.user_0_device_group_0 = self.user_0['device_groups'][0]
        self.user_0_device_group_1 = self.user_0['device_groups'][1]
        self.user_1_device_group_0 = self.user_1['device_groups'][0]
        self.user_1_device_group_1 = self.user_1['device_groups'][1]
        # print(self.user_1_device_group_0['devices'][0])
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_devices_and_data()
        self.TestData.delete_all_users()
    def test_get_device_data_devtype_right_devid_right(self):
        ''' 登录普通用户，传入该用户包含的设备的devtype和devid'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "",1)
        self.assertEqual(self.result,3)
    def test_get_device_data_devtype_right_devid_ls_1(self):
        ''' 登录普通用户，传入该用户包含的设备的devtype和devid少一位字符'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'][:-1],
                                           "",1)
        self.assertEqual(self.result, 404)
    def test_get_device_data_devtype_right_devid_not_exist(self):
        ''' 登录普通用户，传入该用户包含的设备的devtype和d不存在的devid'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],"sgfwetsdf",
                                           "",1)
        self.assertEqual(self.result, 404)
    def test_get_device_data_devtype_right_devid_of_other_user(self):
        ''' 登录普通用户，传入该用户包含的设备的devtype和其他用户包含的设备的devid'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "",1)
        self.assertEqual(self.result, 403)
    def test_get_device_data_devid_right_devtype_ls_1(self):
        ''' 登录普通用户，传入该用户包含的设备的devid和devtype少一位字符'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'][:-1],self.user_0_device_group_0['devices'][0]['devid'],
                                           "",1)
        self.assertEqual(self.result, 400)
    def test_get_device_data_devid_right_devtype_not_exist(self):
        ''' 登录普通用户，传入该用户包含的设备的devid和不存在的devtype'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + 'gedryxfvsr5',self.user_0_device_group_0['devices'][0]['devid'],
                                           "",1)
        self.assertEqual(self.result, 400)
    def test_get_device_data_filter_device_data_arr_0(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[0] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result, 1)
    def test_get_device_data_filter_device_data_arr_1(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[1] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result, 2)
    def test_get_device_data_filter_device_data_arr_2(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[2] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result, 2)
    def test_get_device_data_filter_device_data_arr_3(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[3] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result, 1)
    def test_get_device_data_filter_device_data_arr_4(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[4] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result, 0)
    def test_get_device_data_filter_device_data_arr_4_1(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][1]['devtype'],self.user_0_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[4] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_device_data_arr_5(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][1]['devtype'],self.user_0_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[5] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_device_data_arr_6(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_0['devices'][1]['devtype'],self.user_0_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[6] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,1)
    def test_get_device_data_filter_device_data_arr_7(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][0]['devtype'],self.user_0_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[7] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_device_data_arr_8(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][0]['devtype'],self.user_0_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[8] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_device_data_arr_9(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][0]['devtype'],self.user_0_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[9] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,1)
    def test_get_device_data_filter_device_data_arr_10(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][1]['devtype'],self.user_0_device_group_1['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[10] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_device_data_arr_11(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][1]['devtype'],self.user_0_device_group_1['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[11] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_device_data_arr_12(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_0,"devtype=" + self.user_0_device_group_1['devices'][1]['devtype'],self.user_0_device_group_1['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[12] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,1)
    def test_get_device_data_filter_device_data_arr_13(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[13] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_device_data_arr_14(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[14] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_device_data_arr_15(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[15] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,1)
    def test_get_device_data_filter_device_data_arr_16(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_0['devices'][1]['devtype'],self.user_1_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[16] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_device_data_arr_17(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_0['devices'][1]['devtype'],self.user_1_device_group_0['devices'][1]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[17] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,2)
    def test_get_device_data_filter_device_data_arr_18(self):
        ''' 登录普通用户，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_1['devices'][0]['devtype'],self.user_1_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[18] + "%22%3A0%7D" ,1)
        self.assertEqual(self.result,1)
    def test_get_device_data_not_login(self):
        ''' 不登录，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_1['devices'][0]['devtype'],self.user_1_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[18] + "%22%3A0%7D" ,0)
        self.assertEqual(self.result,401)
    def test_get_device_data_logout(self):
        ''' 登录后再退出，传入该用户包含的设备的数据'''
        self.result = delete_device_data_test(self.base_url,self.user_1,"devtype=" + self.user_1_device_group_1['devices'][0]['devtype'],self.user_1_device_group_1['devices'][0]['devid'],
                                           "&filter=%7B%22"+ device_data_arr[18] + "%22%3A0%7D" ,2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    unittest.main()