# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.test_data import device_event_test_data_arr
'''返回码如下：
            200 操作成功
            400	无效参数
            401 没有登录
            500 服务器内部错误'''
def add_device_event_test(base_url,login_user,payload,login_or_not=1):
    '''参数化编程，login_user：登录的账号，payload：传入的数据，login_or_not：1：登录，0：不登录，2：登录后再退出'''
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not==1:
        user.login()
        r = session.post(base_url,json=payload)
    elif login_or_not == 0:
        r = requests.post(base_url,json=payload)
    else:
        user.login()
        user.logout()
        r = session.post(base_url,json=payload)
    user.login()
    user.delete_all_device_events()
    # if r.status_code == 200:
    #     # print(r.json()['data'])
    #     return r.json()['data']
    # else:
    return r.status_code


class DevicesEventsAddTest(unittest.TestCase):  #####与开发确认数据的取值范围
    '''添加一条设备事件 接口测试'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/events"
        self.TestData = InitialData(83,83,83,85)
        self.users_arr = self.TestData.create_users()
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_device_events()
        self.TestData.delete_all_users()
    def test_add_device_event_right(self):
        '''登录普通用户，传入符合条件的设备事件信息,判断所有返回的信息是否与填入信息一致'''
        payload = {"name": device_event_test_data_arr[0][0],"time": int(device_event_test_data_arr[0][1]),"eventtype": device_event_test_data_arr[0][2],"devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        # self.result = (result['name'] == payload['name'] and result['time'] == payload['time'] and result['eventtype'] == payload['eventtype'] and result['devtype'] == payload['devtype'] and result['devid'] == payload['devid'])
        self.assertEqual(self.result,200)
    def test_add_device_event_temperature_high_error(self):
        '''登录普通用户，传入符合name和eventtype关系不对应'''
        payload = {"name": "temperature_high","time": int(device_event_test_data_arr[0][1]),"eventtype": "error","devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_temperature_too_high_error(self):
        '''登录普通用户，传入符合name=temperature和eventtype=error'''
        payload = {"name": "temperature_too_high","time": int(device_event_test_data_arr[0][1]),"eventtype": "error","devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        # self.result = (result['name'] == payload['name'] and result['time'] == payload['time'] and result['eventtype'] == payload['eventtype'] and result['devtype'] == payload['devtype'] and result['devid'] == payload['devid'])
        self.assertEqual(self.result,200)
    def test_add_device_event_temperature_too_high_warning(self):
        '''登录普通用户，传入符合name=temperature和eventtype=error'''
        payload = {"name": "temperature_too_high","time": int(device_event_test_data_arr[0][1]),"eventtype": "warning","devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_temperature_too_high_ls_1(self):
        '''登录普通用户，传入name=temperature_too_high少一位字符'''
        payload = {"name": "temperature_too_hig","time": int(device_event_test_data_arr[0][1]),"eventtype": "error","devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_temperature_high_ls_1(self):
        '''登录普通用户，传入name=temperature_high少一位字符'''
        payload = {"name": "temperature_hig","time": int(device_event_test_data_arr[0][1]),"eventtype": "warning","devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_warning_ls_1(self):
        '''登录普通用户，传入eventtype=warning少一位字符'''
        payload = {"name": "temperature_high","time": int(device_event_test_data_arr[0][1]),"eventtype": "warnin","devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_error_ls_1(self):
        '''登录普通用户，传入eventtype=error少一位字符'''
        payload = {"name": "temperature_too_high","time": int(device_event_test_data_arr[0][1]),"eventtype": "erro","devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_devtype_ls_1(self):
        '''登录普通用户，传入devtype=inverter少一位字符'''
        payload = {"name": "temperature_high","time": '136454d',"eventtype": "warning","devtype": device_event_test_data_arr[0][3][:-1],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_devdtype_not_exist(self):
        '''登录普通用户，传入不存在的devtype'''
        payload = {"name": "temperature_too_high","time": '136454d',"eventtype": "warning","devtype": 'sadgfsg',"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_devid_ls_1(self):
        '''登录普通用户，传入devid=存在设备的devid少一位字符'''
        payload = {"name": "temperature_too_high","time": '136454d',"eventtype": "warning","devtype": 'devtype',"devid": device_event_test_data_arr[0][4][:-1]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_devid_not_exist(self):
        '''登录普通用户，传入devid=不存在的devid'''
        payload = {"name": "temperature_too_high","time": '136454d',"eventtype": "warning","devtype": 'devtype',"devid": 'fsdgdfvsdfw45dfgcv'}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_name_null(self):
        '''登录普通用户，传入其他符合条件的设备事件信息,不填入name信息'''
        payload = {"time": int(device_event_test_data_arr[0][1]),"eventtype": device_event_test_data_arr[0][2],"devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_time_null(self):
        '''登录普通用户，传入其他符合条件的设备事件信息,不填入time信息'''
        payload = {"name": device_event_test_data_arr[0][0],"eventtype": device_event_test_data_arr[0][2],"devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        # self.result = (result['name'] == payload['name']  and result['eventtype'] == payload['eventtype'] and result['devtype'] == payload['devtype'] and result['devid'] == payload['devid'])
        self.assertEqual(self.result,200)
    def test_add_device_event_eventtype_null(self):
        '''登录普通用户，传入其他符合条件的设备事件信息,不填入eventtype信息'''
        payload = {"name": device_event_test_data_arr[0][0],"time": int(device_event_test_data_arr[0][1]),"devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_devtype_null(self):
        '''登录普通用户，传入其他符合条件的设备事件信息,不填入devtype信息'''
        payload = {"name": device_event_test_data_arr[0][0],"time": int(device_event_test_data_arr[0][1]),"eventtype": device_event_test_data_arr[0][2],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_event_devid_null(self):
        '''登录普通用户，传入其他符合条件的设备事件信息,不填入devid信息'''
        payload = {"name": device_event_test_data_arr[0][0],"time": int(device_event_test_data_arr[0][1]),"eventtype": device_event_test_data_arr[0][2],"devtype": device_event_test_data_arr[0][3]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,400)
    def test_add_device_devid_of_other_user(self):
        '''登录普通用户，传入符合条件的设备事件信息,判断所有返回的信息是否与填入信息一致'''
        payload = {"name": device_event_test_data_arr[0][0],"time": int(device_event_test_data_arr[0][1]),"eventtype": device_event_test_data_arr[0][2],"devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[1][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        # self.result = (result['name'] == payload['name'] and result['time'] == payload['time'] and result['eventtype'] == payload['eventtype'] and result['devtype'] == payload['devtype'] and result['devid'] == payload['devid'])
        self.assertEqual(self.result,200)
    def test_add_device_devid_of_self(self):
        '''登录普通用户，传入符合条件的设备事件信息,判断所有返回的信息是否与填入信息一致'''
        session = requests.Session()
        user = UsersForTest(int(self.users_arr[0]['mobile'][-2:]),session)
        user.login()
        r1 = user.create_device_group({"groupname":"groupname924","desc":"sdgwetdsf"})
        r2 = user.add_device(r1.json()['data']['groupid'],{"devid":device_event_test_data_arr[0][4],"devtype":device_event_test_data_arr[0][3]})
        payload = {"name": device_event_test_data_arr[0][0],"time": int(device_event_test_data_arr[0][1]),"eventtype": device_event_test_data_arr[0][2],"devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,1)
        self.assertEqual(self.result,200)
    def test_add_device_event_not_login(self):
        '''不登录，传入符合条件的设备事件信息,判断所有返回的信息是否与填入信息一致'''
        payload = {"name": device_event_test_data_arr[0][0],"time": int(device_event_test_data_arr[0][1]),"eventtype": device_event_test_data_arr[0][2],"devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,0)
        self.assertEqual(self.result,401)
    def test_add_device_event_logout(self):
        '''登录后退出，传入符合条件的设备事件信息,判断所有返回的信息是否与填入信息一致'''
        payload = {"name": device_event_test_data_arr[0][0],"time": int(device_event_test_data_arr[0][1]),"eventtype": device_event_test_data_arr[0][2],"devtype": device_event_test_data_arr[0][3],"devid": device_event_test_data_arr[0][4]}
        self.result = add_device_event_test(self.base_url,self.users_arr[0],payload,2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    for n in range(83,85):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()


