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
def add_device_data_test(url,login_user,devtype,devid,data,login_or_not=1):
    '''参数化编程，login_user:登录的用户，，login_or_not:是否登录，默认登录'''
    base_url = url + devid + '/data?devtype=' + devtype
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.post(base_url,json=data)
    elif login_or_not == 0:
        r = requests.post(base_url,json=data)
    else:
        user.login()
        user.logout()
        r = session.post(base_url,json=data)
    return r.status_code

class DevicesDataAddTest(unittest.TestCase):   #####与开发确认数据的取值范围
    '''添加设备数据 接口测试
    每个用例前提条件：创建两个用户，每个用户创建两个设备分组，每个设备分组添加两个设备'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/devices/"
        self.TestData = InitialData(69, 69, 69,71)
        self.users_device_groups_devices_data = self.TestData.users_device_groups_devices(2,2)
        self.user_0 = self.users_device_groups_devices_data[0]
        self.user_1 = self.users_device_groups_devices_data[1]
        self.user_0_device_group_0 = self.user_0['device_groups'][0]
        self.user_0_device_group_1 = self.user_0['device_groups'][1]
        self.user_1_device_group_0 = self.user_1['device_groups'][0]
        self.user_1_device_group_1 = self.user_1['device_groups'][1]
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_devices_and_data()
        self.TestData.delete_all_users()
    def test_add_devices_data_right(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入total_energy'''
        data = {"total_energy":0}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_devtype_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype少一位字符，data传入total_energy'''
        data = {"total_energy":0}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'][:-1],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_devtype_wrong(self):
        '''登录普通用户，传入该用户所包含设备的devid和错误的devtype，data传入total_energy'''
        data = {"total_energy":0}
        self.result = add_device_data_test(self.base_url,self.user_0, 'temperature' ,self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_devid_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和错误的devtype，data传入total_energy'''
        data = {"total_energy":0}
        self.result = add_device_data_test(self.base_url,self.user_0, self.user_0_device_group_0['devices'][0]['devtype'] ,self.user_0_device_group_0['devices'][0]['devid'][:-1],data,1)
        self.assertEqual(self.result,404)
    def test_add_devices_data_devid_wrong(self):
        '''登录普通用户，传入该用户所包含设备的devid和错误的devtype，data传入total_energy'''
        data = {"total_energy":0}
        self.result = add_device_data_test(self.base_url,self.user_0, self.user_0_device_group_0['devices'][0]['devtype'] ,'sgedsrgh',data,1)
        self.assertEqual(self.result,404)
    def test_add_devices_data_device_of_other_user(self):
        '''登录普通用户，传入该用户所包含设备的devid和错误的devtype，data传入total_energy'''
        data = {"total_energy":0}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_1_device_group_0['devices'][0]['devtype'],self.user_1_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,403)
    def test_add_devices_data_total_energy_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入total_energy'''
        data = {"total_energ":0}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_total_energy_char(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入total_energy'''
        data = {"total_energ":'0'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_today_enegy(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature'''
        data = {"temperature":0}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_today_energy_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature少一位字符'''
        data = {"today_energ":0}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_today_energy_char(self):       ###存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature为字符串类型'''
        data = {"temperature":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_temperature(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature'''
        data = {"temperature":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_temperature_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature少一位字符'''
        data = {"temperatur":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_temperature_char(self):   #存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature为字符串类型'''
        data = {"temperature":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_temperature_minus(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature为负值'''
        data = {"temperature":-2}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_temperature_0(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature为0'''
        data = {"temperature":0}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_temperature_150(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入temperature为150'''
        data = {"temperature":150}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    #
    def test_add_devices_data_gfci(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入gfci'''
        data = {"gfci":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_gfci_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入gfci少一位字符'''
        data = {"gfc":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_gfci_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入gfci为字符串类型'''
        data = {"gfci":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_gfci_minus(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入gfci为负值'''
        data = {"gfci":-564576476}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_gfci_0(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入gfci为0'''
        data = {"gfci":0}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_gfci_positive(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入gfci为150'''
        data = {"gfci":457568436}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_power(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入power'''
        data = {"power":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_power_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入power少一位字符'''
        data = {"powe":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_power_char(self):     ##存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入power为字符串类型'''
        data = {"power":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_bus_volt(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入bud_volt'''
        data = {"bus_volt":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_bus_volt_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入bud_volt少一位字符'''
        data = {"bud_vol":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_bus_volt_char(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入bud_volt为字符串类型'''
        data = {"bud_volt":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_q_power(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入q_power'''
        data = {"q_power":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_q_power_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入q_power少一位字符'''
        data = {"q_powe":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_q_power_char(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入q_power为字符串类型'''
        data = {"q_power":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_pf(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pf'''
        data = {"pf":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_pf_char(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pf为字符串类型'''
        data = {"pf":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_pv1_volt(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv1_volt'''
        data = {"pv1_volt":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_pv1_volt_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv1_volt为字符串类型'''
        data = {"pv1_volt":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_pv1_curr(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv1_curr'''
        data = {"pv1_curr":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_pv1_curr_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv1_curr为字符串类型'''
        data = {"pv1_curr":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_pv2_volt(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv2_volt'''
        data = {"pv2_volt":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_pv2_volt_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv2_volt为字符串类型'''
        data = {"pv2_volt":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_pv3_volt(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv3_volt'''
        data = {"pv3_volt":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_pv3_volt_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv3_volt为字符串类型'''
        data = {"pv3_volt":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_pv3_curr(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv3_curr'''
        data = {"pv3_curr":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_pv3_curr_char(self):  ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入pv3_curr为字符串类型'''
        data = {"pv3_curr":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_l1_volt(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_volt'''
        data = {"l1_volt":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_l1_volt_char(self):   ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_volt为字符串类型'''
        data = {"l1_volt":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_l1_curr(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_curr'''
        data = {"l1_curr":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_l1_curr_char(self):   ##存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_curr为字符串类型'''
        data = {"l1_curr":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_l1_freq(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_freq'''
        data = {"l1_freq":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_l1_freq_char(self):   ##存在Bug
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_freq为字符串类型'''
        data = {"l1_freq":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_l1_dci(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_dci'''
        data = {"l1_dci":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_l1_dci_char(self):    ##存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_dci为字符串类型'''
        data = {"l1_dci":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_l1_power(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_power'''
        data = {"l1_power":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_l1_power_char(self):  ##存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_power为字符串类型'''
        data = {"l1_power":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_l1_pf(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_pf'''
        data = {"l1_pf":15}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_l1_pf_char(self): ##存在BUG
        '''登录普通用户，传入该用户所包含设备的devid和devtype，data传入l1_pf为字符串类型'''
        data = {"l1_pf":'ab'}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,400)
    def test_add_devices_data_all(self):
        '''登录普通用户，传入该用户所包含设备的devid和devtype'''
        data = {"l1_pf":100,"total_energy":200,"temperature":12,"gfci":4654,"bus_volt":416,"power":4546,"q_power":135,"pf":546,"pv1_volt":154,"pv1_curr":132,"pv2_volt":451,"pv2_curr":465,"pv3_volt":654,"pv3_curr": 454,"l1_volt":4154,"l1_curr":468,"l1_freq": 4854,"l1_dci":465,"l1_power":454}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,1)
        self.assertEqual(self.result,200)
    def test_add_devices_data_not_login(self):
        '''不登录，传入存在的设备的devid和devtype，data传入l1_pf为字符串类型'''
        data = {"l1_pf":45}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,0)
        self.assertEqual(self.result,401)
    def test_add_devices_data_logout(self):
        '''登录后退出，传入存在的设备的devid和devtype，data传入l1_pf为字符串类型'''
        data = {"l1_pf":45}
        self.result = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data,2)
        self.assertEqual(self.result,401)
    def test_add_device_data_add_several_data(self):
        '''添加多个数据'''
        data1 = {"power": 45}
        data2 = {"l1_power":15}
        data3 = {"power": 3454}
        r1 = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data1,1)
        print(r1)
        r2 = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data2,1)
        print(r2)
        r3 = add_device_data_test(self.base_url,self.user_0,self.user_0_device_group_0['devices'][0]['devtype'],self.user_0_device_group_0['devices'][0]['devid'],data3,1)
        print(r3)
        session = requests.Session()
        user = UsersForTest(int(self.user_0['mobile'][-2:]),session)
        r4 = user.login()
        print('login?',r4.status_code)
        result = user.device_data_inquery(devtype=self.user_0_device_group_0['devices'][0]['devtype'],devid=self.user_0_device_group_0['devices'][0]['devid'])
        print(result.json())
        self.result = len(result.json()['data'])
        self.assertEqual(self.result,3)
if __name__ == '__main__':
    for n in range(69,71):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()

